#include "../interface/FCNCTriLeptonCppWorker.h"
#include <iostream>
#include <cmath>

//190306 KST 15:44 : just copy this code from FCNCTriLeptonCppWorker.cc
//
using namespace std;

FCNCTriLeptonCppWorker::FCNCTriLeptonCppWorker(const std::string modeName, const bool doNonPromptLepton):
  doNonPromptLepton_(doNonPromptLepton)
{
  if ( modeName == "MuElEl" ) mode_ = MODE::MuElEl;
  else if ( modeName == "ElMuMu" ) mode_ = MODE::ElMuMu;
  else if ( modeName == "ElElEl" ) mode_ = MODE::ElElEl;
  else if ( modeName == "MuMuMu" ) mode_ = MODE::MuMuMu;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. " << endl;
    mode_ = MODE::None;//This should be changed kind of 'return false...'(do not run this worker)
  }
}

typedef FCNCTriLeptonCppWorker::TRAF TRAF;
typedef FCNCTriLeptonCppWorker::TRAI TRAI;
typedef FCNCTriLeptonCppWorker::TRAB TRAB;

void FCNCTriLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                                          TRAF relIso, TRAI id, TRAF dEtaSC, TRAF eCorr, TRAI vidBitmap) {
  in_Electrons_p4[0] = pt;
  in_Electrons_p4[1] = eta;
  in_Electrons_p4[2] = phi;
  in_Electrons_p4[3] = mass;
  in_Electrons_charge = charge;
  in_Electrons_relIso = relIso;
  in_Electrons_id = id;
  in_Electrons_dEtaSC = dEtaSC;
  in_Electrons_eCorr = eCorr;
  in_Electrons_vidBitmap = vidBitmap;
}

void FCNCTriLeptonCppWorker::setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
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

void FCNCTriLeptonCppWorker::setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
                                         TRAI id, TRAF CSVv2) {
  in_Jet_p4[0] = pt;
  in_Jet_p4[1] = eta;
  in_Jet_p4[2] = phi;
  in_Jet_p4[3] = mass;
  in_Jet_CSVv2 = CSVv2;
  in_Jet_id = id;
}

void FCNCTriLeptonCppWorker::setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi) {
  in_MET_pt = pt;
  in_MET_phi = phi;
}

void FCNCTriLeptonCppWorker::resetValues() {
  for ( unsigned i=0; i<4; ++i ) {
    out_Lepton1_p4[i] = out_Lepton2_p4[i] = out_Lepton3_p4[i] = 0;
    out_LeadingMuon_p4[i] = out_LeadingElectron_p4[i] = 0;
    out_Z_p4[i] = 0;
  }
  out_Lepton1_pdgId = out_Lepton2_pdgId = out_Lepton3_pdgId = 0;
  out_TriLepton_mass = out_TriLepton_pt = 0;
  out_TriLepton_WleptonZdPhi = out_TriLepton_WleptonZdR = 0;
  out_Z_charge = 0;
  out_MET_pt = out_MET_phi = 0;
  out_W_MT = 0;
  out_GoodLeptonCode = out_nVetoLepton = 0;
  out_nGoodJet = out_nBjet = 0;
  for ( int i=0; i<4; ++i ) out_GoodJet_p4[i].clear();
  out_GoodJet_CSVv2.clear();
  out_GoodJet_index.clear();

}
//signal muons
bool FCNCTriLeptonCppWorker::isGoodMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( in_Muons_isTight->At(i) == 0 ) return false;
  if ( in_Muons_relIso->At(i) > maxMuonRelIso_ ) return false; //maxMuonRelIso : Tight PF isolation value

  return true;
}
//veto muons
bool FCNCTriLeptonCppWorker::isVetoMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( ! ( in_Muons_isPFcand->At(i) != 0 and (in_Muons_isGlobal->At(i) != 0 or in_Muons_isTracker->At(i) != 0) ) ) return false;
  if ( in_Muons_relIso->At(i) > maxVetoMuonRelIso_ ) return false; //maxVetoMuonRelIso : Loose PF isolation value

  return true;
}
//nonprompt muons
bool FCNCTriLeptonCppWorker::isNPMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( ! ( in_Muons_isPFcand->At(i) != 0 and (in_Muons_isGlobal->At(i) != 0 or in_Muons_isTracker->At(i) != 0) ) ) return false;
  if ( in_Muons_relIso->At(i) < maxMuonRelIso_ ) return false;

  return true; 
}

//signal electrons
bool FCNCTriLeptonCppWorker::isGoodElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  const double scEta = eta + in_Electrons_dEtaSC->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  if ( std::abs(scEta) > 1.4442 and std::abs(scEta) < 1.566 ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
  if ( in_Electrons_id->At(i) != 4 ) return false;

  return true;
}
//veto electrons
bool FCNCTriLeptonCppWorker::isVetoElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  const double scEta = eta + in_Electrons_dEtaSC->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  if ( std::abs(scEta) > 1.4442 and std::abs(scEta) < 1.566 ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
  if ( in_Electrons_id->At(i) == 0 ) return false;

  return true;
}
//nonprompt electrons: 191018 for now pending about NP electron
bool FCNCTriLeptonCppWorker::isNPElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  const double scEta = eta + in_Electrons_dEtaSC->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  if ( std::abs(scEta) > 1.4442 and std::abs(scEta) < 1.566 ) return false;
  //nanoAOD object -> Electron_vidNestedWPBitmapSum16 (total 10 cuts in here by bitmap, each cut has 3 bit)
  const unsigned vidBitmap = in_Electrons_vidBitmap->At(i);
  for ( unsigned i=0; i<10; ++i ) {
    // 0x7 = 111 in the binary representation
    // after the bitwise operations, 3 bits to store cuts. 0:fail, 1:veto, 2:loose, 3:medium, 4:tight
    const unsigned vidBit = (vidBitmap & (0x7<<(3*i))) >> (3*i);

    if      ( i == 2 ) { if ( vidBit >= 4 ) return false; } // invert isolation
    else if ( i == 3 ) { if ( vidBit <  4 ) return false; } // require tight 1/E-1/p cut
    else if ( vidBit < 2 ) return false;
  }

  return true;
}

bool FCNCTriLeptonCppWorker::isGoodJet(const unsigned i) const {
  const double pt = in_Jet_p4[0]->At(i);
  const double eta = in_Jet_p4[1]->At(i);
  if ( pt < minJetPt_ or std::abs(eta) > maxJetEta_ ) return false;
  if ( in_Jet_id->At(i) == 0 ) return false;

  return true;
}

TLorentzVector FCNCTriLeptonCppWorker::buildP4(const TRAF p4Arr[], const unsigned i) const {
  TLorentzVector p4;
  p4.SetPtEtaPhiM(p4Arr[0]->At(i), p4Arr[1]->At(i), p4Arr[2]->At(i), p4Arr[3]->At(i));
  return p4;
}

void FCNCTriLeptonCppWorker::setOutputP4(float outP4[], const float inP4[]) {
  for ( unsigned i=0; i<4; ++i ) outP4[i] = inP4[i];
}

void FCNCTriLeptonCppWorker::setOutputP4(float outP4[], const TLorentzVector& p4) {
  outP4[0] = p4.Pt();
  outP4[1] = p4.Eta();
  outP4[2] = p4.Phi();
  outP4[3] = p4.M();
}

double FCNCTriLeptonCppWorker::computeMT(const TLorentzVector& lepP4, const double met_pt, const double met_phi) const {
  //MET_px = MET_pt*cos(phi) & MET_py = MET_pt*sin(phi)
  const double met_px = met_pt*cos(met_phi);
  const double met_py = met_pt*sin(met_phi);

  const double pt = lepP4.Pt() + met_pt;
  const double px = lepP4.Px() + met_px;
  const double py = lepP4.Py() + met_py;

  return std::sqrt(std::max(0., pt*pt - px*px - py*py));
}

bool FCNCTriLeptonCppWorker::analyze() {
  resetValues();

  // Start from trivial stuffs
  out_MET_pt = **in_MET_pt;
  out_MET_phi = **in_MET_phi;

  // Select leptons
  std::vector<unsigned> muonIdxs;
  std::vector<unsigned> electronIdxs;
  int npMuonIdx = -1, npElectronIdx = -1;
  double npMuonPt = 0, npElectronPt = 0;
  unsigned nVetoMuons = 0, nVetoElectrons = 0;
  for ( unsigned i=0, n=in_Muons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodMuon(i) ) muonIdxs.push_back(i);
    //if ( isVetoMuon(i) ) ++nVetoMuons;
    if ( isGoodMuon(i) ) ++nVetoMuons; // NTU's simplified analysis
    const double pt = in_Muons_p4[0]->At(i);
    if ( doNonPromptLepton_ and isNPMuon(i) and npMuonPt < pt ) {
      npMuonIdx = i;
      npMuonPt = pt;
    }
  }
  for ( unsigned i=0, n=in_Electrons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodElectron(i) ) electronIdxs.push_back(i);
    //if ( isVetoElectron(i) ) ++nVetoElectrons;
    if ( isGoodElectron(i) ) ++nVetoElectrons; // NTU's simplified analysis
    const double pt = in_Electrons_p4[0]->At(i);
    if ( doNonPromptLepton_ and isNPElectron(i) and npElectronPt < pt ) {
      npElectronIdx = i;
      npElectronPt = pt;
    }
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
  TLorentzVector lepton1P4, lepton2P4, lepton3P4;

  // Select event by decay mode
  auto actualMode = mode_;
  if ( actualMode == MODE::MuElEl ) {
    if ( actualMode == MODE::MuElEl and nGoodMuons >= 1 ) {
      lepton1P4 = buildP4(in_Muons_p4, muonIdxs[0]);
      out_Lepton1_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
      setOutputP4(out_LeadingMuon_p4, lepton1P4);
    }
    if ( nGoodElectrons >= 1 ) {
      lepton2P4 = buildP4(in_Electrons_p4, electronIdxs[0]);
      out_Lepton2_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
      setOutputP4(out_LeadingElectron_p4, lepton2P4);
    }
    if ( nGoodElectrons >= 2 ) {
      lepton3P4 = buildP4(in_Electrons_p4, electronIdxs[1]);
      out_Lepton3_pdgId = -11*in_Electrons_charge->At(electronIdxs[1]);
    }
  }
  else if ( actualMode == MODE::ElMuMu ) {
    if ( actualMode == MODE::ElMuMu and nGoodElectrons >= 1 ) {
      lepton1P4 = buildP4(in_Electrons_p4, electronIdxs[0]);
      out_Lepton1_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
      setOutputP4(out_LeadingElectron_p4, lepton1P4);
    }
    if ( nGoodMuons     >= 1 ) {
      lepton2P4 = buildP4(in_Muons_p4, muonIdxs[0]);
      out_Lepton2_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
      setOutputP4(out_LeadingMuon_p4, lepton2P4);
    }
    if ( nGoodMuons     >= 2 ) {
      lepton3P4 = buildP4(in_Muons_p4, muonIdxs[1]);
      out_Lepton3_pdgId = -13*in_Muons_charge->At(muonIdxs[1]);
    }
  }
  else if ( actualMode == MODE::ElElEl ) {
    if ( nGoodElectrons >= 1 ) {
      lepton1P4 = buildP4(in_Electrons_p4, electronIdxs[0]);
      out_Lepton1_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
      setOutputP4(out_LeadingElectron_p4, lepton1P4);
    }
    if ( nGoodElectrons >= 2 ) {
      lepton2P4 = buildP4(in_Electrons_p4, electronIdxs[1]);
      out_Lepton2_pdgId = -11*in_Electrons_charge->At(electronIdxs[1]);
    }
    if ( nGoodElectrons >= 3 ) {
      lepton3P4 = buildP4(in_Electrons_p4, electronIdxs[2]);
      out_Lepton3_pdgId = -11*in_Electrons_charge->At(electronIdxs[2]);
    }
  }
  else if ( actualMode == MODE::MuMuMu ) {
    if ( nGoodMuons >= 1 ) {
      lepton1P4 = buildP4(in_Muons_p4, muonIdxs[0]);
      out_Lepton1_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
      setOutputP4(out_LeadingMuon_p4, lepton1P4);
    }
    if ( nGoodMuons >= 2 ) {
      lepton2P4 = buildP4(in_Muons_p4, muonIdxs[1]);
      out_Lepton2_pdgId = -13*in_Muons_charge->At(muonIdxs[1]);
    }
    if ( nGoodMuons >= 3 ) {
      lepton3P4 = buildP4(in_Muons_p4, muonIdxs[2]);
      out_Lepton3_pdgId = -13*in_Muons_charge->At(muonIdxs[2]);
    }
  }

  // For the NPL selection: use one lepton with inverted isolation for the 3rd lepton
  if ( doNonPromptLepton_ ) {
    // Treat 3rd lepton as veto lepton, which is isolated
    if ( std::abs(out_Lepton3_pdgId) == 13 ) ++nVetoMuons;
    else if ( std::abs(out_Lepton3_pdgId) == 11 ) ++nVetoElectrons;

    if ( npMuonIdx >= 0 and std::abs(out_Lepton3_pdgId) != 11 ) {
      lepton3P4 = buildP4(in_Muons_p4, npMuonIdx);
      out_Lepton3_pdgId = -13*in_Muons_charge->At(npMuonIdx);
    }
    else if ( npElectronIdx >= 0 and std::abs(out_Lepton3_pdgId) != 13 ) {
      lepton3P4 = buildP4(in_Electrons_p4, npElectronIdx);
      out_Lepton3_pdgId = -11*in_Electrons_charge->At(npElectronIdx);
    }
    else {
      lepton3P4 = TLorentzVector();
      out_Lepton3_pdgId = 0;
    }
  }

  // Done for the leptons

  out_GoodLeptonCode = 0; // GoodLepton "code". 
  //leading lepton> 25GeV, 2nd,3rd lepton> 20GeV (in GoodMu, Ele object: just >20GeV cut applied)
  // 111: all matched with the desired channel/mode
  // -111: all matched with the desired channel/mode but wrong sign
  // 110: missing one lepton  
  // 101: missing one lepton
  // 100: missing two same flavour leptons for muee/emumu
  // 001: missing two of three leptons for eee/mumumu, two different flav leptons for muee/emumu
  // 000: no leptons found in this event
  if ( out_Lepton1_pdgId ) out_GoodLeptonCode += 100;
  if ( out_Lepton2_pdgId ) out_GoodLeptonCode +=  10;
  if ( out_Lepton3_pdgId ) out_GoodLeptonCode +=   1;

  TLorentzVector leptonTotP4;
  leptonTotP4 = lepton1P4+lepton2P4+lepton3P4;
  out_TriLepton_mass = leptonTotP4.M();
  out_TriLepton_pt = leptonTotP4.Pt();

  // Rearrange lepton1,lepton2,lepton3 to fit to our purpose
  if ( out_GoodLeptonCode >= 111 and
       (actualMode == MODE::MuMuMu or actualMode == MODE::ElElEl ) ) {
/*
    // Algorithm1: arrange by charge
    // Rearrange leptons to form charge configurations like +(+-)
    // -> swap lepton1 and lepton2 if +(--) or -(++) => -(+-) / +(-+)
    if ( out_Lepton2_pdgId*out_Lepton3_pdgId > 0 and out_Lepton1_pdgId*out_Lepton2_pdgId < 0 ) {
      std::swap(lepton1P4, lepton2P4);
      std::swap(out_Lepton1_pdgId, out_Lepton2_pdgId);
    }
*/
    // Algorithm2: arrange by mass
    // Rearrange leptons to have dilepton mass closest to the Z mass
    // -> try all three combinations and choose the best one
    const double dm12 = std::abs((lepton1P4+lepton2P4).M()-91.2);
    const double dm23 = std::abs((lepton2P4+lepton3P4).M()-91.2);
    const double dm31 = std::abs((lepton3P4+lepton1P4).M()-91.2);
    if ( dm12 < dm23 and dm12 < dm31 ) {
      const TLorentzVector tmpP4 = lepton3P4; // (1,2,3) -> (3,1,2)
      lepton3P4 = lepton2P4;
      lepton2P4 = lepton1P4;
      lepton1P4 = tmpP4;
      const int tmpPdgId = out_Lepton3_pdgId;
      out_Lepton3_pdgId = out_Lepton2_pdgId;
      out_Lepton2_pdgId = out_Lepton1_pdgId;
      out_Lepton1_pdgId = tmpPdgId;
    }
    else if ( dm31 < dm12 and dm31 < dm23 ) {
      const TLorentzVector tmpP4 = lepton3P4; // (1,2,3) -> (2,1,3)
      std::swap(lepton1P4, lepton2P4);
      std::swap(out_Lepton1_pdgId, out_Lepton2_pdgId);
    }
  }
  if ( out_GoodLeptonCode >= 100 ) setOutputP4(out_Lepton1_p4, lepton1P4);
  if ( out_GoodLeptonCode >= 110 ) setOutputP4(out_Lepton2_p4, lepton2P4);
  if ( out_GoodLeptonCode >= 111 ) setOutputP4(out_Lepton3_p4, lepton3P4);

  // Check the sign of Z-candidate. Flip the sign for the same-signed lepton pair
  if ( out_Lepton2_pdgId*out_Lepton3_pdgId > 0 ) out_GoodLeptonCode *= -1;

  // Build Z candidate (save non-zero charge of Z bosons together for bkg. estimation)
  if ( std::abs(out_GoodLeptonCode) % 100 == 11 ) {
    const TLorentzVector zP4 = lepton2P4+lepton3P4;
    out_Z_p4[0] = zP4.Pt();
    out_Z_p4[1] = zP4.Eta();
    out_Z_p4[2] = zP4.Phi();
    out_Z_p4[3] = zP4.M();

    const int sumId = out_Lepton2_pdgId+out_Lepton3_pdgId;
    if      ( sumId <= (-11-11) ) out_Z_charge = +2;
    else if ( sumId >= (+11+11) ) out_Z_charge = -2;
    else if ( sumId <= -11 ) out_Z_charge = +1;
    else if ( sumId >= +11 ) out_Z_charge = -1;

    out_TriLepton_WleptonZdPhi = lepton1P4.DeltaPhi(zP4);
    out_TriLepton_WleptonZdR   = lepton1P4.DeltaR(zP4);
  }

  // Transeverse mass of the W boson
  //Lepton comes from W which has high pT
  if ( std::abs(out_GoodLeptonCode) >= 100 ) {
    out_W_MT = computeMT(lepton1P4, out_MET_pt, out_MET_phi);
  }

  // Continue to the Jets
  std::vector<unsigned short> jetIdxs;
  jetIdxs.reserve(in_Jet_CSVv2->GetSize());
  for ( unsigned i=0, n=in_Jet_CSVv2->GetSize(); i<n; ++i ) {
    if ( !isGoodJet(i) ) continue;
    TLorentzVector jetP4 = buildP4(in_Jet_p4, i);
    if ( lepton1P4.Pt() > 0 and lepton1P4.DeltaR(jetP4) < 0.35 ) continue;
    if ( lepton2P4.Pt() > 0 and lepton2P4.DeltaR(jetP4) < 0.35 ) continue;
    if ( lepton3P4.Pt() > 0 and lepton3P4.DeltaR(jetP4) < 0.35 ) continue;
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

