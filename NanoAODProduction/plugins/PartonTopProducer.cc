#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"
#include "RecoJets/JetProducers/interface/JetSpecific.h"

#include "TZWi/NanoAODProduction/interface/TTbarModeDefs.h"

#include <numeric>

using namespace std;

class PartonTopProducer : public edm::stream::EDProducer<>
{
public:
  PartonTopProducer(const edm::ParameterSet& pset);
  void produce(edm::Event& event, const edm::EventSetup& eventSetup) override;

private:
  const reco::Candidate* getLast(const reco::Candidate* p) const;
  const reco::Candidate* getFirst(const reco::Candidate* p) const;
  reco::GenParticleRef buildGenParticle(const reco::Candidate* p, reco::GenParticleRefProd& refHandle,
                                        std::unique_ptr<reco::GenParticleCollection>& outColl) const;

  typedef reco::Particle::LorentzVector LorentzVector;

  const double jetMinPt_, jetMaxEta_;
  typedef fastjet::JetDefinition JetDef;
  std::shared_ptr<JetDef> fjDef_;
  const reco::Particle::Point genVertex_;

private:
  edm::EDGetTokenT<edm::View<reco::Candidate> > genParticleToken_;
};

PartonTopProducer::PartonTopProducer(const edm::ParameterSet& pset):
  jetMinPt_(pset.getParameter<double>("jetMinPt")),
  jetMaxEta_(pset.getParameter<double>("jetMaxEta")),
  genVertex_(0,0,0)
{
  genParticleToken_ = consumes<edm::View<reco::Candidate> >(pset.getParameter<edm::InputTag>("genParticles"));
  const double jetConeSize = pset.getParameter<double>("jetConeSize");
  fjDef_ = std::shared_ptr<JetDef>(new JetDef(fastjet::antikt_algorithm, jetConeSize));

  produces<reco::GenParticleCollection>();
  produces<int>("channel");
  produces<std::vector<int> >("modes");

  produces<reco::GenJetCollection>("qcdJets");
}

void PartonTopProducer::produce(edm::Event& event, const edm::EventSetup& eventSetup)
{
  std::unique_ptr<reco::GenParticleCollection> partons(new reco::GenParticleCollection);
  auto partonRefHandle = event.getRefBeforePut<reco::GenParticleCollection>();

  std::unique_ptr<int> channel(new int(TZWi::CH_NOTT));
  std::unique_ptr<std::vector<int> > modes(new std::vector<int>());

  std::unique_ptr<reco::GenJetCollection> qcdJets(new reco::GenJetCollection);

  edm::Handle<edm::View<reco::Candidate> > genParticleHandle;
  if ( event.isRealData() or !event.getByToken(genParticleToken_, genParticleHandle) ) {
    event.put(std::move(partons));
    event.put(std::move(channel), "channel");
    event.put(std::move(modes), "modes");
    event.put(std::move(qcdJets), "qcdJets");
    return;
  }

  // Collect vector and scalar bosons. Keep the boson and its top-mother. nullptr for orphans
  std::vector<std::pair<const reco::Candidate*, const reco::Candidate*>> v2tPairs;
  std::vector<int> qcdParticleIdxs;
  for ( size_t i=0, n=genParticleHandle->size(); i<n; ++i ) {
    const reco::Candidate& p = genParticleHandle->at(i);
    const int status = p.status();
    if ( status == 1 ) continue;

    const int absPdgId = abs(p.pdgId());
    if ( absPdgId >= 23 and absPdgId <= 25 ) { // For Z/W/H
      const reco::Candidate* mo = p.mother();
      // Skip: We will not pick up this if it is a same copy or a radiation product
      if ( mo and mo->pdgId() == p.pdgId() ) continue;

      // Case0: Simplest case, an orphan by definition - no additional action

      // Case1: Mother is not a top quark
      if ( mo and abs(mo->pdgId()) != 6 ) mo = nullptr;

      // Case2: Orphan if number of mother is not 1.
      //        Particles produced from incident beam / partons
      //          ex) q---\.
      //                   +--- V
      //              q'--/
      //        For the t-channels, we also terminate tracking because mother-daughter relationship has no meaning.
      //          ex) q--+----              q-----+---
      //                  \q  (case2)  vs        /q (case3)
      //              q'---+~~ V            q'--+~~~~ V
      if ( p.numberOfMothers() != 1 ) mo = nullptr;

      // Case3: Has copy of mother among its sisters.
      //        appears in a t-channel diagram (drawing above)
      if ( mo ) {
        for ( int j=0, m=mo->numberOfDaughters(); j<m; ++j ) {
          const reco::Candidate* sister = mo->daughter(j);
          if ( sister == &p ) continue;
          if ( sister->pdgId() == mo->pdgId() ) { mo = nullptr; break; }
        }
      }

      v2tPairs.emplace_back(&p, mo);
    }
    else if ( absPdgId < 6 or absPdgId == 21 ) {
      // QCD particles : select one after parton shower, before hadronization
      bool toKeep = true;
      for ( size_t j=0, m=p.numberOfDaughters(); j<m; ++j ) {
        const int absDauId = abs(p.daughter(j)->pdgId());
        if ( absDauId < 6 or absPdgId == 21 ) { toKeep = false; break; } // do not keep if it is final parton
      }
      if ( toKeep ) qcdParticleIdxs.push_back(i);
    }
  }

  // Build top quark decay tree in parton level
  // Also determine decay mode from parton level information
  size_t nElectronTotal = 0, nMuonTotal = 0, nTauTotal = 0;

  // Fill ther top quarks first place
  std::map<const reco::Candidate*, reco::GenParticleRef> tRefMap;
  std::vector<std::pair<const reco::Candidate*, reco::GenParticleRef>> vvPairs;
  for ( auto& v2tPair : v2tPairs ) {
    //const reco::Candidate* vFirst = v2tPair.first;
    const reco::Candidate* tLast = v2tPair.second;
    if ( tLast == nullptr ) continue;
    reco::GenParticleRef tRef = buildGenParticle(tLast, partonRefHandle, partons);
    tRefMap[tLast] = tRef;
  }

  // Continue to the orphan bosons
  for ( auto& v2tPair : v2tPairs ) {
    const reco::Candidate* vFirst = v2tPair.first;
    const reco::Candidate* tLast = v2tPair.second;
    if ( tLast != nullptr ) continue;
    reco::GenParticleRef vRef = buildGenParticle(vFirst, partonRefHandle, partons);
    vvPairs.emplace_back(vFirst, vRef);
  }

  // Fill the top quark decay products
  for ( auto& v2tPair : v2tPairs ) {
    const reco::Candidate* vFirst = v2tPair.first;
    const reco::Candidate* tLast  = v2tPair.second;
    if ( tLast == nullptr ) continue;

    reco::GenParticleRef vRef;
    vRef = buildGenParticle(vFirst, partonRefHandle, partons);
    auto& tRef = tRefMap[tLast];
    partons->at(vRef.key()).addMother(tRef);
    partons->at(tRef.key()).addDaughter(vRef);
    vvPairs.emplace_back(vFirst, vRef);

    const reco::Candidate* qFirst = nullptr;
    for ( int j=0, m=tLast->numberOfDaughters(); j<m; ++j ) {
      const reco::Candidate* dau = tLast->daughter(j);
      const unsigned int dauAbsId = abs(dau->pdgId());
      if ( dauAbsId < 6 ) { qFirst = dau; break; }
    }

    if ( qFirst != nullptr ) {
      reco::GenParticleRef qRef = buildGenParticle(qFirst, partonRefHandle, partons);
      partons->at(qRef.key()).addMother(tRef);
      partons->at(tRef.key()).addDaughter(qRef);
    }
  }

  // Fill the V-decay products no matter it is an orphan or from top
  for ( auto& vvPair : vvPairs ) {
    const reco::Candidate* vFirst = vvPair.first;
    const reco::Candidate* vLast = getLast(vFirst);
    reco::GenParticleRef vRef = vvPair.second;

    // V-decay products
    std::vector<const reco::Candidate*> vDaus;
    for ( int j=0, m=vLast->numberOfDaughters(); j<m; ++j ) {
      const reco::Candidate* vDau = vLast->daughter(j);
      const unsigned int dauAbsId = abs(vDau->pdgId());
      if ( vLast->pdgId() != 25 and dauAbsId > 16 ) continue; // Consider quarks and leptons only for W/Z decays
      // With the line above, we allow H->ff/GG/ZZ/WW.
      // vLast should be W/Z/H, nothing else.

      vDaus.push_back(vDau);
    }
    if ( vDaus.empty() ) continue;
    std::sort(vDaus.begin(), vDaus.end(), [](const reco::Candidate* vDau1, const reco::Candidate* vDau2){
              return abs(vDau1->pdgId()) < abs(vDau2->pdgId());});
    std::vector<reco::GenParticleRef> vDauRefs;
    for ( auto vDau : vDaus ) {
      reco::GenParticleRef vDauRef = buildGenParticle(vDau, partonRefHandle, partons);
      partons->at(vDauRef.key()).addMother(vRef);
      partons->at(vRef.key()).addDaughter(vDauRef);
      vDauRefs.push_back(vDauRef);
    }

    // Special care for FCNH, H->WW or H->ZZ because we have to add one more intermediate step
    std::vector<const reco::Candidate*> v2vDaus;
    std::vector<reco::GenParticleRef> v2vDauRefs;
    for ( size_t i=0, n=vDaus.size(); i<n; ++i ) {
      const reco::Candidate* vDau = vDaus.at(i);
      const int absDauId = abs(vDau->pdgId());
      if ( absDauId != 23 and absDauId != 24 ) continue;

      reco::GenParticleRef vDauRef = vDauRefs.at(i);
      const reco::Candidate* vDauLast = getLast(vDau);
      for ( size_t j=0, m=vDauLast->numberOfDaughters(); j<m; ++j ) {
        const reco::Candidate* v2vDau = vDauLast->daughter(j);
        reco::GenParticleRef v2vDauRef = buildGenParticle(v2vDau, partonRefHandle, partons);
        partons->at(v2vDauRef.key()).addMother(vDauRef);
        partons->at(vDauRef.key()).addDaughter(v2vDauRef);
        v2vDauRefs.push_back(v2vDauRef);
        v2vDaus.push_back(v2vDau);
      }
    }

    // Append v2vDaus to the existing vDaus collection, to account tau->lepton decays
    vDaus.insert(vDaus.end(), v2vDaus.begin(), v2vDaus.end());
    vDauRefs.insert(vDauRefs.end(), v2vDauRefs.begin(), v2vDauRefs.end());

    // Special care for tau->lepton decays
    // Note : we do not keep neutrinos from tau decays (tau->W, nu_tau, W->l, nu_l)
    // Note : Up to 6 neutrinos from top decays if both W decays to taus and all taus go into leptonic decay chain
    int nElectron = 0, nMuon = 0, nTau = 0;
    for ( size_t i=0, n=vDaus.size(); i<n; ++i ) {
      const reco::Candidate* vDau = vDaus.at(i);

      const int aid = abs(vDau->pdgId());
      if      ( aid == 11 ) ++nElectron;
      else if ( aid == 13 ) ++nMuon;
      else if ( aid == 15 ) ++nTau;

      if ( aid != 15 ) continue;

      std::vector<const reco::Candidate*> lepsFromTau;

      const reco::Candidate* tauLast = getLast(vDau);
      for ( int j=0, m=tauLast->numberOfDaughters(); j<m; ++j ) {
        const reco::Candidate* dau = tauLast->daughter(j);
        const unsigned int dauAbsId = abs(dau->pdgId());
        if ( dauAbsId == 11 or dauAbsId == 13 ) lepsFromTau.push_back(dau);
      }

      // Skip if net charge is zero. This happens if a conversion photon is radiated (tau->gamma+X, gamma->e+e-)
      // This happens in sub-per-mil level (observed 6 among 10000 events)
      // Note: tau->hadrons are automatically skipped with this sumQ != 0 condition.
      const int sumQ = std::accumulate(lepsFromTau.begin(), lepsFromTau.end(), 0, [](int b, const reco::Candidate* a){return a->charge()+b;});
      if ( sumQ == 0 ) continue;

      reco::GenParticleRef vDauRef = vDauRefs.at(i);

      // Sort daughter leptons, largest pT with consistent electric charge to the original tau at the front.
      std::sort(lepsFromTau.begin(), lepsFromTau.end(), [](const reco::Candidate* a, const reco::Candidate* b){return a->pt() > b->pt();});
      std::stable_sort(lepsFromTau.begin(), lepsFromTau.end(), [&](const reco::Candidate* a, const reco::Candidate* b){return a->charge() == tauLast->charge();});
      for ( auto lepFromTau : lepsFromTau ) {
        reco::GenParticleRef lepRef = buildGenParticle(lepFromTau, partonRefHandle, partons);
        partons->at(lepRef.key()).addMother(vDauRef);
        partons->at(vDauRef.key()).addDaughter(lepRef);
      }
    }

    int mode = TZWi::CH_HADRON;
    if      ( nElectron >= 1 and nMuon == 0 ) mode = TZWi::CH_ELECTRON;
    else if ( nElectron == 0 and nMuon >= 1 ) mode = TZWi::CH_MUON;
    else if ( nElectron >= 1 and nMuon >= 1 ) mode = TZWi::CH_MUONELECTRON;
    if ( nTau >= 1 ) mode += TZWi::CH_TAU_HADRON;

    nElectronTotal += nElectron;
    nMuonTotal += nMuon;
    nTauTotal += nTau;

    modes->push_back(mode);
  }

  if ( modes->size() == 2 ) {
    const int nLepton = nElectronTotal + nMuonTotal;
    if      ( nLepton == 0 ) *channel = TZWi::CH_FULLHADRON;
    else if ( nLepton == 1 ) *channel = TZWi::CH_SEMILEPTON;
    else if ( nLepton == 2 ) *channel = TZWi::CH_FULLLEPTON;
    else *channel = TZWi::CH_MULTILEPTON;
  }

  // Make genJets using particles after PS, but before hadronization
  std::vector<fastjet::PseudoJet> fjInputs;
  fjInputs.reserve(qcdParticleIdxs.size());
  for ( int i : qcdParticleIdxs ) {
    const auto& p = genParticleHandle->at(i);
    fjInputs.push_back(fastjet::PseudoJet(p.px(), p.py(), p.pz(), p.energy()));
    fjInputs.back().set_user_index(i);
  }
  fastjet::ClusterSequence fjClusterSeq(fjInputs, *fjDef_);
  std::vector<fastjet::PseudoJet> fjJets = fastjet::sorted_by_pt(fjClusterSeq.inclusive_jets(jetMinPt_));
  qcdJets->reserve(fjJets.size());
  for ( auto& fjJet : fjJets ) {
    if ( abs(fjJet.eta()) > jetMaxEta_ ) continue;
    const auto& fjCons = fjJet.constituents();
    std::vector<reco::CandidatePtr> cons;
    cons.reserve(fjCons.size());
    for ( auto con : fjCons ) {
      const size_t index = con.user_index();
      cons.push_back(genParticleHandle->ptrAt(index));
    }

    const LorentzVector jetP4(fjJet.px(), fjJet.py(), fjJet.pz(), fjJet.E());
    reco::GenJet qcdJet;
    reco::writeSpecific(qcdJet, jetP4, genVertex_, cons, eventSetup);
    qcdJet.setPdgId(0);
    for ( auto& con : cons ) {
      const int absPdgId = abs(con->pdgId());
      if ( (absPdgId == 5 or absPdgId == 4) and (abs(qcdJet.pdgId()) < absPdgId) ) {
        qcdJet.setPdgId(con->pdgId());
      }
    }

    qcdJets->push_back(qcdJet);
  }

  event.put(std::move(partons));
  event.put(std::move(channel), "channel");
  event.put(std::move(modes), "modes");
  event.put(std::move(qcdJets), "qcdJets");
}

const reco::Candidate* PartonTopProducer::getFirst(const reco::Candidate* p) const
{
  const reco::Candidate* mo = p->mother();
  if ( mo != nullptr and p->pdgId() == mo->pdgId() ) return getFirst(mo);
  return p;
}

const reco::Candidate* PartonTopProducer::getLast(const reco::Candidate* p) const
{
  int nDecay = 0;
  std::vector<const reco::Candidate*> sameCopies;
  for ( size_t i=0, n=p->numberOfDaughters(); i<n; ++i ) {
    const reco::Candidate* dau = p->daughter(i);
    const int dauId = dau->pdgId();
    if ( dauId == 22 or dauId == 21 ) continue;
    if ( p->pdgId() == dau->pdgId() ) sameCopies.push_back(dau);
    else ++nDecay;
  }
  if ( nDecay == 0 ) {
    for ( const auto dau : sameCopies ) {
      if ( p->pdgId() == dau->pdgId() ) return getLast(dau);
    }
  }
  return p;
}

reco::GenParticleRef PartonTopProducer::buildGenParticle(const reco::Candidate* p, reco::GenParticleRefProd& refHandle,
                                                         std::unique_ptr<reco::GenParticleCollection>& outColl) const
{
  reco::GenParticle pOut(*dynamic_cast<const reco::GenParticle*>(p));
  pOut.clearMothers();
  pOut.clearDaughters();
  pOut.resetMothers(refHandle.id());
  pOut.resetDaughters(refHandle.id());

  outColl->push_back(pOut);

  return reco::GenParticleRef(refHandle, outColl->size()-1);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PartonTopProducer);

