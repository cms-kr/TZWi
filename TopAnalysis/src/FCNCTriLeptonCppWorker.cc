#include "../interface/FCNCTriLeptonCppWorker.h"
#include <iostream>
#include <cmath>

//190306 KST 15:44 : just copy this code from FCNCTriLeptonCppWorker.cc
//
using namespace std;

FCNCTriLeptonCppWorker::FCNCTriLeptonCppWorker(const std::string modeName)
{
  if ( modeName == "ElElMu" ) mode_ = MODE::ElElMu;
  else if ( modeName == "MuMuEl" ) mode_ = MODE::MuMuEl;
  else if ( modeName == "ElElEl" ) mode_ = MODE::ElElEl;
  else if ( modeName == "MuMuMu" ) mode_ = MODE::MuMuMu;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. " << endl;
    mode_ = MODE::None;//This should be changed kind of 'return false...'(do not run this worker)
  }
}

void FCNCTriLeptonCppWorker::initOutput(TTree *outputTree){
  if ( _doCppOutput ) return;

  //if (_doCppOutput) throw cms::Exception("LogicError","doCppOutput cannot be called twice");
  _doCppOutput = true;

  const std::array<std::string, 4> varNames = {{"pt", "eta", "phi", "mass"}};
  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Lepton1_%s", varNames[i].c_str()), &out_Lepton1_p4[i], Form("Lepton1_%s/F", varNames[i].c_str()));
  }
  outputTree->Branch("Lepton1_pdgId", &out_Lepton1_pdgId, "Lepton1_pdgId/I");
  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Lepton2_%s", varNames[i].c_str()), &out_Lepton2_p4[i], Form("Lepton2_%s/F", varNames[i].c_str()));
  }
  outputTree->Branch("Lepton2_pdgId", &out_Lepton2_pdgId, "Lepton2_pdgId/I");

  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Lepton3_%s", varNames[i].c_str()), &out_Lepton3_p4[i], Form("Lepton3_%s/F", varNames[i].c_str()));
  }
  outputTree->Branch("Lepton3_pdgId", &out_Lepton3_pdgId, "Lepton3_pdgId/I");

  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Z_%s", varNames[i].c_str()), &out_Z_p4[i], Form("Z_%s/F", varNames[i].c_str()));
  }
  outputTree->Branch("Z_charge", &out_Z_charge, "Z_charge/S");

  outputTree->Branch("MET_pt", &out_MET_pt, "MET_pt/F");
  outputTree->Branch("MET_phi", &out_MET_phi, "MET_phi/F");

  outputTree->Branch("W_TrMass", &out_W_TrMass, "W_TrMass/F");

  outputTree->Branch("nGoodJets", &out_nGoodJets, "nGoodJets/s");
  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Jets_%s", varNames[i].c_str()), out_Jets_p4[i], Form("Jets_%s[nGoodJets]/F", varNames[i].c_str()));
  }
  outputTree->Branch("Jets_CSVv2", out_Jets_CSVv2, "Jets_CSVv2[nGoodJets]/F");
  outputTree->Branch("nGoodBjets", &out_nGoodBjets, "nGoodBjets/s");

  outputTree->Branch("CutStep", &out_CutStep, "CutStep/s");
}

typedef FCNCTriLeptonCppWorker::TRAF TRAF;
typedef FCNCTriLeptonCppWorker::TRAI TRAI;
typedef FCNCTriLeptonCppWorker::TRAB TRAB;

void FCNCTriLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
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
  in_Jets_p4[0] = pt;
  in_Jets_p4[1] = eta;
  in_Jets_p4[2] = phi;
  in_Jets_p4[3] = mass;
  in_Jets_CSVv2 = CSVv2;
  in_Jets_id = id;
}

void FCNCTriLeptonCppWorker::setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi) {
  in_MET_pt = pt;
  in_MET_phi = phi;
}

void FCNCTriLeptonCppWorker::resetValues() {
  for ( unsigned i=0; i<4; ++i ) {
    out_Lepton1_p4[i] = out_Lepton2_p4[i] = out_Lepton3_p4[i] = 0;
  }
  out_Lepton1_pdgId = out_Lepton2_pdgId = out_Lepton3_pdgId = 0;
  out_MET_pt = out_MET_phi = 0;
  out_W_TrMass = 0;
  out_nGoodJets = out_nGoodBjets = 0;
  for ( unsigned k=0; k<maxNGoodJetsToKeep_; ++k ) {
    for ( unsigned i=0; i<4; ++i ) out_Jets_p4[i][k] = 0;
  }
  out_CutStep = 0;
}
//signal muons
bool FCNCTriLeptonCppWorker::isGoodMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( in_Muons_isTight == 0 ) return false;
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
//signal electrons
bool FCNCTriLeptonCppWorker::isGoodElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i) * in_Electrons_eCorr->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:medium, 3:tight
  if ( in_Electrons_id->At(i) != 3 ) return false;

  return true;
}
//veto electrons
bool FCNCTriLeptonCppWorker::isVetoElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i) * in_Electrons_eCorr->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  //nanoAOD object -> Electron_cutBased_Sum16 0:fail, 1:veto, 2:medium, 3:tight
  if ( in_Electrons_id->At(i) == 0 ) return false;

  return true;
}

bool FCNCTriLeptonCppWorker::isGoodJet(const unsigned i) const {
  const double pt = in_Jets_p4[0]->At(i);
  const double eta = in_Jets_p4[1]->At(i);
  if ( pt < minJetPt_ or std::abs(eta) > maxJetEta_ ) return false;
  if ( in_Jets_id->At(i) == 0 ) return false;

  return true;
}

TLorentzVector FCNCTriLeptonCppWorker::buildP4(const TRAF p4Arr[], unsigned i) const {
  TLorentzVector p4;
  p4.SetPtEtaPhiM(p4Arr[0]->At(i), p4Arr[1]->At(i), p4Arr[2]->At(i), p4Arr[3]->At(i));
  return p4;
}

double FCNCTriLeptonCppWorker::computeMT(const TLorentzVector& lepP4, const double met_pt, const double met_phi) const
{
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
  std::vector<int> muonIdxs;
  std::vector<int> electronIdxs;
  for ( unsigned i=0, n=in_Muons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodMuon(i) ) muonIdxs.push_back(i);
  }
  for ( unsigned i=0, n=in_Electrons_p4[0]->GetSize(); i<n; ++i ) {
    if ( isGoodElectron(i) ) electronIdxs.push_back(i);
  }
  const int nGoodMuons = muonIdxs.size();
  const int nGoodElectrons = electronIdxs.size();
  if ( nGoodMuons+nGoodElectrons < 3 ) return false; // Require at least three leptons.

  std::sort(muonIdxs.begin(), muonIdxs.end(), [&](const int i, const int j){
              return in_Muons_p4[0]->At(i) > in_Muons_p4[0]->At(j);});
  std::sort(electronIdxs.begin(), electronIdxs.end(), [&](const int i, const int j){
              return in_Electrons_p4[0]->At(i)*in_Electrons_eCorr->At(i) >
                     in_Electrons_p4[0]->At(j)*in_Electrons_eCorr->At(j);});

  // Select event by decay mode
  auto actualMode = mode_;
  if ( actualMode == MODE::ElElMu ) {
    if ( nGoodElectrons < 2 and nGoodMuons < 1 ) return false;
    if ( in_Electrons_charge->At(electronIdxs[0]) == in_Electrons_charge->At(electronIdxs[1]) ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Electrons_p4[i]->At(electronIdxs[0]);
      out_Lepton2_p4[i] = in_Electrons_p4[i]->At(electronIdxs[1]);
      out_Lepton3_p4[i] = in_Muons_p4[i]->At(muonIdxs[0]);
    }
    out_Lepton1_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
    out_Lepton2_pdgId = -11*in_Electrons_charge->At(electronIdxs[1]);
    out_Lepton3_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
  }
  else if ( actualMode == MODE::MuMuEl ) {
    if ( nGoodElectrons < 1 and nGoodMuons < 2 ) return false;
    if ( in_Muons_charge->At(muonIdxs[0]) == in_Muons_charge->At(muonIdxs[1]) ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Muons_p4[i]->At(muonIdxs[0]);
      out_Lepton2_p4[i] = in_Muons_p4[i]->At(muonIdxs[1]);
      out_Lepton3_p4[i] = in_Electrons_p4[i]->At(electronIdxs[0]);
    }
    out_Lepton1_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
    out_Lepton2_pdgId = -13*in_Muons_charge->At(muonIdxs[1]);
    out_Lepton3_pdgId = -11*in_Electrons_charge->At(electronIdxs[1]);
  }
  else if ( actualMode == MODE::ElElEl ) {
    if ( nGoodElectrons < 3 ) return false;
    if ( in_Electrons_charge->At(electronIdxs[0]) == in_Electrons_charge->At(electronIdxs[1]) ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Electrons_p4[i]->At(electronIdxs[0]);
      out_Lepton2_p4[i] = in_Electrons_p4[i]->At(electronIdxs[1]);
      out_Lepton3_p4[i] = in_Electrons_p4[i]->At(electronIdxs[2]);
    }
    out_Lepton1_pdgId = -11*in_Electrons_charge->At(electronIdxs[0]);
    out_Lepton2_pdgId = -11*in_Electrons_charge->At(electronIdxs[1]);
    out_Lepton3_pdgId = -11*in_Electrons_charge->At(electronIdxs[2]);
  }
  else if ( actualMode == MODE::MuMuMu ) {
    if ( nGoodMuons < 3 ) return false;
    if ( in_Muons_charge->At(muonIdxs[0]) == in_Muons_charge->At(muonIdxs[1]) ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Muons_p4[i]->At(muonIdxs[0]);
      out_Lepton2_p4[i] = in_Muons_p4[i]->At(muonIdxs[1]);
      out_Lepton3_p4[i] = in_Muons_p4[i]->At(muonIdxs[2]);
    }
    out_Lepton1_pdgId = -13*in_Muons_charge->At(muonIdxs[0]);
    out_Lepton2_pdgId = -13*in_Muons_charge->At(muonIdxs[1]);
    out_Lepton3_pdgId = -13*in_Muons_charge->At(muonIdxs[2]);
  }

  TLorentzVector lepton1P4, lepton2P4, lepton3P4;
  lepton1P4.SetPtEtaPhiM(out_Lepton1_p4[0], out_Lepton1_p4[1], out_Lepton1_p4[2], out_Lepton1_p4[3]);
  lepton2P4.SetPtEtaPhiM(out_Lepton2_p4[0], out_Lepton2_p4[1], out_Lepton2_p4[2], out_Lepton2_p4[3]);
  lepton3P4.SetPtEtaPhiM(out_Lepton3_p4[0], out_Lepton3_p4[1], out_Lepton3_p4[2], out_Lepton3_p4[3]);
  // Done for the leptons

  // Build Z candidate
  const auto zP4 = lepton1P4+lepton2P4;
  out_Z_p4[0] = zP4.Pt();
  out_Z_p4[1] = zP4.Eta();
  out_Z_p4[2] = zP4.Phi();
  out_Z_p4[3] = zP4.M();
  out_Z_charge = out_Lepton1_pdgId+out_Lepton2_pdgId;
  out_Z_charge = out_Z_charge == 0 ? 0 : 2*out_Z_charge/abs(out_Z_charge);

  // Transeverse mass of the W boson
  //if lepton3 comes from W (that lepton have high pT)
  out_W_TrMass = computeMT(lepton3P4, out_MET_pt, out_MET_phi);

  // Continue to the Jets
  std::vector<unsigned short> jetIdxs;
  jetIdxs.reserve(in_Jets_CSVv2->GetSize());
  for ( unsigned i=0, n=in_Jets_CSVv2->GetSize(); i<n; ++i ) {
    if ( !isGoodJet(i) ) continue;
    TLorentzVector jetP4 = buildP4(in_Jets_p4, i);
    if ( lepton1P4.DeltaR(jetP4) < 0.3 ) continue;
    if ( lepton2P4.DeltaR(jetP4) < 0.3 ) continue;
    if ( lepton3P4.DeltaR(jetP4) < 0.3 ) continue;
    jetIdxs.push_back(i);
    if ( in_Jets_CSVv2->At(i) > minGoodBjetBDiscr_ ) ++out_nGoodBjets;
  }
  out_nGoodJets = jetIdxs.size();
  if ( out_nGoodJets < int(minEventNGoodJets_) ) return false;
  if ( out_nGoodBjets < int(minEventNGoodBjets_) ) return false;

  // Sort jets by pt
  std::sort(jetIdxs.begin(), jetIdxs.end(),
            [&](const unsigned short i, const unsigned short j){ return in_Jets_p4[0]->At(i) > in_Jets_p4[0]->At(j); });
  for ( unsigned k=0, n=std::min(maxNGoodJetsToKeep_, out_nGoodJets); k<n; ++k ) {
    const unsigned kk = jetIdxs.at(k);
    for ( unsigned i=0; i<4; ++i ) out_Jets_p4[i][k] = in_Jets_p4[i]->At(kk);
    out_Jets_CSVv2[k] = in_Jets_CSVv2->At(kk);
  }

  // Get CutStep
  out_CutStep = 0;
  // do-while trick, to reduce nested-if statements
  do {
    if ( !(out_nGoodJets >= 1 and out_nGoodJets <= 3) ) break;
    ++out_CutStep;
    if ( !(out_W_TrMass < 300) ) break;
    ++out_CutStep;
/*
    // Z-veto and MET (no cut for e-mu channel)
    if ( actualMode == MODE::MuEl ) {
      out_CutStep += 2;
    }
    else {
      if ( out_Z_p4[0] > 75 or out_Z_p4[0] < 105 ) break;
      ++out_CutStep;
      if ( out_MET_pt < 40 ) break;
      ++out_CutStep;
    }
*/
  } while ( false );

  return true;
}

