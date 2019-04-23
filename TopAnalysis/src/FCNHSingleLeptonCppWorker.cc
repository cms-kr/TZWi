#include "../interface/FCNHSingleLeptonCppWorker.h"
#include <iostream>
#include <cmath>

//190306 KST 15:44 : just copy this code from FCNHSingleLeptonCppWorker.cc
//
using namespace std;

FCNHSingleLeptonCppWorker::FCNHSingleLeptonCppWorker(const std::string modeName)
{
  if ( modeName == "Mu" ) mode_ = MODE::Mu;
  else if ( modeName == "El" ) mode_ = MODE::El;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. " << endl;
    mode_ = MODE::None;//This should be changed kind of 'return false...'(do not run this worker)
  }
}

typedef FCNHSingleLeptonCppWorker::TRAF TRAF;
typedef FCNHSingleLeptonCppWorker::TRAI TRAI;
typedef FCNHSingleLeptonCppWorker::TRAB TRAB;

void FCNHSingleLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                                          TRAF relIso, TRAI id, TRAF dEtaSC, TRAF eCorr) {
  in_Electrons_p4[0] = pt;
  in_Electrons_p4[1] = eta;
  in_Electrons_p4[2] = phi;
  in_Electrons_p4[3] = mass;
  in_Electrons_charge = charge;
  in_Electrons_relIso = relIso;
  in_Electrons_id = id;
  in_Electrons_dEtaSC = dEtaSC;
  in_Electrons_eCorr = eCorr;
}

void FCNHSingleLeptonCppWorker::setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                                      TRAF relIso, TRAB isTight, TRAB isGlobal, TRAB isPFcand, TRAB isTracker) {
  in_Muons_p4[0] = pt;
  in_Muons_p4[1] = eta;
  in_Muons_p4[2] = phi;
  in_Muons_p4[3] = mass;
  in_Muons_charge = charge;
  in_Muons_relIso = relIso;
  in_Muons_isTight = isTight;
  in_Muons_isGlobal = isGlobal;
  in_Muons_isPFcand = isPFcand;
  in_Muons_isTracker = isTracker;
}

void FCNHSingleLeptonCppWorker::setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
                                     TRAI id, TRAF CSVv2) {
  in_Jet_p4[0] = pt;
  in_Jet_p4[1] = eta;
  in_Jet_p4[2] = phi;
  in_Jet_p4[3] = mass;
  in_Jet_CSVv2 = CSVv2;
  in_Jet_id = id;
}

void FCNHSingleLeptonCppWorker::setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi) {
  in_MET_pt = pt;
  in_MET_phi = phi;
}

void FCNHSingleLeptonCppWorker::resetValues() {
  for ( unsigned i=0; i<4; ++i ) {
    out_Lepton_p4[i] = 0;
  }
  out_Lepton_pdgId = 0;
  out_MET_pt = out_MET_phi = 0;
  out_nGoodJet = out_nBjet = 0;
  for ( int i=0; i<4; ++i ) out_GoodJet_p4[i].clear();
  out_GoodJet_CSVv2.clear();
  out_GoodJet_index.clear();

}
//signal muons
bool FCNHSingleLeptonCppWorker::isGoodMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( in_Muons_isTight->At(i) == 0 ) return false;
  if ( in_Muons_relIso->At(i) > maxMuonRelIso_ ) return false; //maxMuonRelIso : Tight PF isolation value

  return true;
}
//veto muons
bool FCNHSingleLeptonCppWorker::isVetoMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( ! ( in_Muons_isPFcand->At(i) != 0 and (in_Muons_isGlobal->At(i) != 0 or in_Muons_isTracker->At(i) != 0) ) ) return false;
  if ( in_Muons_relIso->At(i) > maxVetoMuonRelIso_ ) return false; //maxVetoMuonRelIso : Loose PF isolation value

  return true;
}
//signal electrons
bool FCNHSingleLeptonCppWorker::isGoodElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
  if ( in_Electrons_id->At(i) != 4 ) return false;

  return true;
}
//veto electrons
bool FCNHSingleLeptonCppWorker::isVetoElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
  if ( in_Electrons_id->At(i) == 0 ) return false;

  return true;
}

bool FCNHSingleLeptonCppWorker::isGoodJet(const unsigned i) const {
  const double pt = in_Jet_p4[0]->At(i);
  const double eta = in_Jet_p4[1]->At(i);
  if ( pt < minJetPt_ or std::abs(eta) > maxJetEta_ ) return false;
  if ( in_Jet_id->At(i) == 0 ) return false;

  return true;
}

TLorentzVector FCNHSingleLeptonCppWorker::buildP4(const TRAF p4Arr[], unsigned i) const {
  TLorentzVector p4;
  p4.SetPtEtaPhiM(p4Arr[0]->At(i), p4Arr[1]->At(i), p4Arr[2]->At(i), p4Arr[3]->At(i));
  return p4;
}

bool FCNHSingleLeptonCppWorker::analyze() {
  resetValues();

  // Start from trivial stuffs
  out_MET_pt = **in_MET_pt;
  out_MET_phi = **in_MET_phi;

  // Select leptons
  std::vector<int> muonIdxs;
  std::vector<int> electronIdxs;
  unsigned nVetoMuons = 0, nVetoElectrons = 0;
  for ( unsigned i=0, n=in_Muons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodMuon(i) ) muonIdxs.push_back(i);
    if ( isVetoMuon(i) ) ++nVetoMuons;
  }
  for ( unsigned i=0, n=in_Electrons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodElectron(i) ) electronIdxs.push_back(i);
    if ( isVetoElectron(i) ) ++nVetoElectrons;
  }
  std::sort(muonIdxs.begin(), muonIdxs.end(), [&](const int i, const int j){
              return in_Muons_p4[0]->At(i) > in_Muons_p4[0]->At(j);});
  std::sort(electronIdxs.begin(), electronIdxs.end(), [&](const int i, const int j){
              return in_Electrons_p4[0]->At(i) > in_Electrons_p4[0]->At(j);});

  const int nGoodMuons = muonIdxs.size();
  const int nGoodElectrons = electronIdxs.size();
  nVetoMuons -= nGoodMuons;
  nVetoElectrons -= nGoodElectrons;
  out_nVetoLepton = nVetoMuons + nVetoElectrons;

  // Select event by decay mode
  auto actualMode = mode_;
  if ( actualMode == MODE::Mu ) {
    for ( unsigned i=0; i<4; ++i ) {
        if ( nGoodMuons     >= 1 ) out_Lepton_p4[i] = in_Muons_p4[i]->At(muonIdxs[0]);
    }
    if ( nGoodMuons     >= 1 ) out_Lepton_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
  }
  else if ( actualMode == MODE::El ) {
    for ( unsigned i=0; i<4; ++i ) {
        if ( nGoodElectrons >= 1 ) out_Lepton_p4[i] = in_Electrons_p4[i]->At(electronIdxs[0]);
    }
    if ( nGoodElectrons >= 1 ) out_Lepton_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
  }

  TLorentzVector leptonP4; //Lepton has the largest pt among the three leptons.
  leptonP4.SetPtEtaPhiM(out_Lepton_p4[0], out_Lepton_p4[1], out_Lepton_p4[2], out_Lepton_p4[3]);
  // Done for the leptons

  // Continue to the Jets
  std::vector<unsigned short> jetIdxs;
  jetIdxs.reserve(in_Jet_CSVv2->GetSize());
  for ( unsigned i=0, n=in_Jet_CSVv2->GetSize(); i<n; ++i ) {
    if ( !isGoodJet(i) ) continue;
    TLorentzVector jetP4 = buildP4(in_Jet_p4, i);
    if ( leptonP4.Pt() > 0 and leptonP4.DeltaR(jetP4) < 0.3 ) continue;
    jetIdxs.push_back(i);
    if ( in_Jet_CSVv2->At(i) > minBjetBDiscr_ ) ++out_nBjet;
  }
  out_nGoodJet = jetIdxs.size();
  // Sort jets by pt
  std::sort(jetIdxs.begin(), jetIdxs.end(),
            [&](const unsigned short i, const unsigned short j){ return in_Jet_p4[0]->At(i) > in_Jet_p4[0]->At(j); });
  for ( unsigned k=0, n=out_nGoodJet; k<n; ++k ) {
    const unsigned kk = jetIdxs.at(k);
    for ( int i=0; i<4; ++i ) out_GoodJet_p4[i].push_back(in_Jet_p4[i]->At(kk));
    out_GoodJet_CSVv2.push_back(in_Jet_CSVv2->At(kk));
    out_GoodJet_index.push_back(kk);
  }

  return true;
}

