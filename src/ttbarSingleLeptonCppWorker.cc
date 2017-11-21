#include "../interface/ttbarSingleLeptonCppWorker.h"
#include <iostream>
#include <cmath>

using namespace std;

ttbarSingleLeptonCppWorker::ttbarSingleLeptonCppWorker(const std::string modeName, const std::string algoName) {
  if      ( modeName == "Auto"     ) mode_ = MODE::Auto;
  else if ( modeName == "Electron" ) mode_ = MODE::Electron;
  else if ( modeName == "Muon"     ) mode_ = MODE::Muon;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. Fall back to \"Auto\"" << endl;
    mode_ = MODE::Auto;
  }

  if      ( algoName == "CloseMTop" ) algo_ = ALGO::CloseMTop;
  else {
    cerr << "Algo name \"" << algoName << "\" is not available. Fall back to \"CloseMTop\"" << endl;
    algo_ = ALGO::CloseMTop;
  }
}

ttbarSingleLeptonCppWorker::~ttbarSingleLeptonCppWorker() {
}

void ttbarSingleLeptonCppWorker::initOutput(TTree *outputTree){
  if ( _doCppOutput ) return;

  //if (_doCppOutput) throw cms::Exception("LogicError","doCppOutput cannot be called twice");
  _doCppOutput = true;

  const std::array<std::string, 4> varNames = {{"pt", "eta", "phi", "mass"}};
  for ( int i=0; i<4; ++i ) outputTree->Branch(Form("Lepton_%s", varNames[i].c_str()), &out_Lepton_p4[i], Form("Lepton_%s/F", varNames[i].c_str()));
  outputTree->Branch("Lepton_pdgId", &out_Lepton_pdgId, "Lepton_pdgId/I");

  outputTree->Branch("MET_pt", &out_MET_pt, "MET_pt/F");
  outputTree->Branch("MET_phi", &out_MET_phi, "MET_phi/F");

  for ( unsigned i=0; i<4; ++i ) outputTree->Branch(Form("LepT_%s", varNames[i].c_str()), &out_LepT_p4[i], Form("LepT_%s/F", varNames[i].c_str()));
  for ( unsigned i=0; i<4; ++i ) outputTree->Branch(Form("HadT_%s", varNames[i].c_str()), &out_HadT_p4[i], Form("HadT_%s/F", varNames[i].c_str()));
  for ( unsigned i=0; i<4; ++i ) outputTree->Branch(Form("LepW_%s", varNames[i].c_str()), &out_LepW_p4[i], Form("LepW_%s/F", varNames[i].c_str()));
  for ( unsigned i=0; i<4; ++i ) outputTree->Branch(Form("HadW_%s", varNames[i].c_str()), &out_HadW_p4[i], Form("HadW_%s/F", varNames[i].c_str()));
  outputTree->Branch("nAddJets", &out_nAddJets, "nAddJets/i");
  for ( unsigned i=0; i<4; ++i ) outputTree->Branch(Form("AddJets_%s", varNames[i].c_str()), &out_AddJets_p4[i], Form("AddJets_%s[nAddJets]/F", varNames[i].c_str()));

  outputTree->Branch("LepTJ0_bDiscr", &out_LepTJ0_bDiscr, "LepTJ0_bDiscr/F");
  outputTree->Branch("HadTJ0_bDiscr", &out_HadTJ0_bDiscr, "HadTJ0_bDiscr/F");
  outputTree->Branch("HadWJ1_bDiscr", &out_HadWJ1_bDiscr, "HadWJ1_bDiscr/F");
  outputTree->Branch("HadWJ2_bDiscr", &out_HadWJ2_bDiscr, "HadWJ2_bDiscr/F");
  outputTree->Branch("AddJets_bDiscr", out_AddJets_bDiscr, "AddJets_bDiscr[nAddJets]/F");

  outputTree->Branch("LepTJ0_bDeepB", &out_LepTJ0_bDeepB, "LepTJ0_bDeepB/F");
  outputTree->Branch("HadTJ0_bDeepB", &out_HadTJ0_bDeepB, "HadTJ0_bDeepB/F");
  outputTree->Branch("HadWJ1_bDeepB", &out_HadWJ1_bDeepB, "HadWJ1_bDeepB/F");
  outputTree->Branch("HadWJ2_bDeepB", &out_HadWJ2_bDeepB, "HadWJ2_bDeepB/F");
  outputTree->Branch("AddJets_bDeepB", out_AddJets_bDeepB, "AddJets_bDeepB[nAddJets]/F");

  outputTree->Branch("LepTJ0_bDeepC", &out_LepTJ0_bDeepC, "LepTJ0_bDeepC/F");
  outputTree->Branch("HadTJ0_bDeepC", &out_HadTJ0_bDeepC, "HadTJ0_bDeepC/F");
  outputTree->Branch("HadWJ1_bDeepC", &out_HadWJ1_bDeepC, "HadWJ1_bDeepC/F");
  outputTree->Branch("HadWJ2_bDeepC", &out_HadWJ2_bDeepC, "HadWJ2_bDeepC/F");
  outputTree->Branch("AddJets_bDeepC", out_AddJets_bDeepC, "AddJets_bDeepC[nAddJets]/F");

  outputTree->Branch("AddJets12_dR", &out_AddJets12_dR, "AddJets12_dR/F");
  outputTree->Branch("AddJets12_mass", &out_AddJets12_mass, "AddJets12_mass/F");
}

typedef ttbarSingleLeptonCppWorker::TRAF TRAF;
typedef ttbarSingleLeptonCppWorker::TRAI TRAI;
typedef ttbarSingleLeptonCppWorker::TRAB TRAB;

void ttbarSingleLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                                              TRAF relIso, TRAI id, TRAI idTrg, TRAF dEtaSC) {
  in_Electrons_p4[0] = pt;
  in_Electrons_p4[1] = eta;
  in_Electrons_p4[2] = phi;
  in_Electrons_p4[3] = mass;
  in_Electrons_charge = charge;
  in_Electrons_relIso = relIso;
  in_Electrons_id = id;
  in_Electrons_idTrg = idTrg;
  in_Electrons_dEtaSC = dEtaSC;
}

void ttbarSingleLeptonCppWorker::setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge, 
                                          TRAF relIso, TRAB id) {
  in_Muons_p4[0] = pt;
  in_Muons_p4[1] = eta;
  in_Muons_p4[2] = phi;
  in_Muons_p4[3] = mass;
  in_Muons_charge = charge;
  in_Muons_relIso = relIso;
  in_Muons_id = id;
}

void ttbarSingleLeptonCppWorker::setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
                                         TRAI id, TRAF bDiscr, TRAF bDeepB, TRAF bDeepC) {
  in_Jets_p4[0] = pt;
  in_Jets_p4[1] = eta;
  in_Jets_p4[2] = phi;
  in_Jets_p4[3] = mass;
  in_Jets_bDiscr = bDiscr;
  in_Jets_id = id;
  in_Jets_bDeepB = bDeepB;
  in_Jets_bDeepC = bDeepC;
}

void ttbarSingleLeptonCppWorker::setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi) {
  in_MET_pt = pt;
  in_MET_phi = phi;
}

void ttbarSingleLeptonCppWorker::resetValues() {
  for ( int i=0; i<4; ++i ) {
    out_Lepton_p4[i] = 0;
    out_LepT_p4[i] = 0;
    out_HadT_p4[i] = 0;
    out_LepW_p4[i] = 0;
    out_HadW_p4[i] = 0;
  }
  out_LepTJ0_bDiscr = out_HadTJ0_bDiscr = 0;
  out_HadWJ1_bDiscr = out_HadWJ2_bDiscr = 0;

  out_LepTJ0_bDeepB = out_HadTJ0_bDeepB = 0;
  out_HadWJ1_bDeepB = out_HadWJ2_bDeepB = 0;

  out_LepTJ0_bDeepC = out_HadTJ0_bDeepC = 0;
  out_HadWJ1_bDeepC = out_HadWJ2_bDeepC = 0;

  out_nAddJets = 0;
  for ( unsigned j=0; j<nMaxAddJets_; ++j ) {
    for ( unsigned i=0; i<4; ++i ) out_AddJets_p4[i][j] = 0;
    out_AddJets_bDiscr[j] = 0;
    out_AddJets_bDeepB[j] = 0;
    out_AddJets_bDeepC[j] = 0;
  }
  out_AddJets12_dR = out_AddJets12_mass = 0;

  out_Lepton_pdgId = 0;
  out_MET_pt = out_MET_phi = 0;
}

bool ttbarSingleLeptonCppWorker::isGoodMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minMuonPt_ or std::abs(eta) > maxMuonEta_ ) return false;
  if ( in_Muons_id->At(i) == 0 ) return false;
  if ( in_Muons_relIso->At(i) < 0.15 ) return false;

  return true;
}

bool  ttbarSingleLeptonCppWorker::isVetoMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minVetoMuonPt_ or std::abs(eta) > maxVetoMuonEta_ ) return false;
  if ( in_Muons_id->At(i) == 0 ) return false; // FIXME: to be replaced with loose cut?
  if ( in_Muons_relIso->At(i) < 0.20 ) return false;

  return true;
}

bool ttbarSingleLeptonCppWorker::isGoodElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minElectronPt_ or std::abs(eta) > maxElectronEta_ ) return false;
  if ( in_Electrons_id->At(i) == 0 or in_Electrons_idTrg->At(i) == 0 ) return false;
  //if ( in_Electrons_relIso->At(i) < 0.15 ) return false; // Note: commented out since already applied in Cut based ID

  return true;
}

bool ttbarSingleLeptonCppWorker::isVetoElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minVetoElectronPt_ or std::abs(eta) > maxVetoElectronEta_ ) return false;
  if ( in_Electrons_id->At(i) == 0 or in_Electrons_idTrg->At(i) == 0 ) return false; // FIXME: to be replaced with loose cut?
  //if ( in_Electrons_relIso->At(i) < 0.15 ) return false; // Note: commneted out since already applied in Cut based ID

  return true;
}

bool ttbarSingleLeptonCppWorker::isGoodJet(const unsigned i) const {
  const double pt = in_Jets_p4[0]->At(i);
  const double eta = in_Jets_p4[1]->At(i);
  if ( pt < minJetPt_ or std::abs(eta) > maxJetEta_ ) return false;
  if ( in_Jets_id->At(i) == 0 ) return false;

  return true;
}

TLorentzVector ttbarSingleLeptonCppWorker::buildP4(const TRAF p4Arr[], unsigned i) const {
  TLorentzVector p4;
  p4.SetPtEtaPhiM(p4Arr[0]->At(i), p4Arr[1]->At(i), p4Arr[2]->At(i), p4Arr[3]->At(i));
  return p4;
}

bool ttbarSingleLeptonCppWorker::analyze() {
  resetValues();

  // Start from trivial stuffs
  out_MET_pt = **in_MET_pt;
  out_MET_phi = **in_MET_phi;

  // Select the leading lepton, veto event if there is 2nd one
  double leadMuonPt = 0;
  int leadMuonIdx = -1, vetoMuon1Idx = -1, vetoMuon2Idx = -1;
  for ( int i=0, n=in_Muons_p4[0]->GetSize(); i<n; ++i ) {
    const double pt = in_Muons_p4[0]->At(i);
    if ( isGoodMuon(i) and pt > leadMuonPt ) {
      leadMuonPt = pt;
      leadMuonIdx = i;
    }
    if ( isVetoMuon(i) ) {
      if ( vetoMuon1Idx < 0 ) vetoMuon1Idx = i;
      else if ( vetoMuon2Idx < 0 or pt > in_Muons_p4[0]->At(vetoMuon2Idx) ) {
        vetoMuon2Idx = i;
        if ( pt > in_Muons_p4[0]->At(vetoMuon1Idx) ) std::swap(vetoMuon1Idx, vetoMuon2Idx);
      }
    }
  }
  double leadElectronPt = 0;
  int leadElectronIdx = -1, vetoElectron1Idx = -1, vetoElectron2Idx = -1;
  for ( int i=0, n=in_Electrons_p4[0]->GetSize(); i<n; ++i ) {
    const double pt = in_Electrons_p4[0]->At(i);
    if ( isGoodElectron(i) and pt > leadElectronPt ) {
      leadElectronPt = pt;
      leadElectronIdx = i;
    }
    if ( isVetoElectron(i) ) {
      if ( vetoElectron1Idx < 0 ) vetoElectron1Idx = i;
      else if ( vetoElectron2Idx < 0 or pt > in_Electrons_p4[0]->At(vetoElectron2Idx) ) {
        vetoElectron2Idx = i;
        if ( pt > in_Electrons_p4[0]->At(vetoElectron1Idx) ) std::swap(vetoElectron1Idx, vetoElectron2Idx);
      }
    }
  }
  // Select event by decay mode
  if ( leadMuonIdx == -1 and leadElectronIdx == -1 ) return false; // At least one selected lepton
  if ( leadMuonIdx != -1 and leadElectronIdx != -1 ) return false; // But also veto dilepton
  // Code below can be written alternatively with minimizing code duplication, but I'm keeping it as simple to be understood.
  if ( mode_ == MODE::Muon ) {
    if ( leadMuonIdx == -1 ) return false;
    if ( vetoElectron1Idx != -1 ) return false;
    if      ( vetoMuon1Idx != -1 and vetoMuon1Idx != leadMuonIdx ) return false;
    else if ( vetoMuon2Idx != -1 and vetoMuon2Idx != leadMuonIdx ) return false;
    //out_Lepton_pdgId = -13*in_Muons_charge[leadMuonIdx];
    for ( unsigned i=0; i<4; ++i ) out_Lepton_p4[i] = in_Muons_p4[i]->At(leadMuonIdx);
  }
  else if ( mode_ == MODE::Electron ) {
    if ( leadElectronIdx == -1 ) return false;
    if ( vetoMuon1Idx != -1 ) return false;
    if      ( vetoElectron1Idx != -1 and vetoElectron1Idx != leadElectronIdx ) return false;
    else if ( vetoElectron2Idx != -1 and vetoElectron2Idx != leadElectronIdx ) return false;
    //out_Lepton_pdgId = -11*in_Electrons_charge->At(leadMuonIdx);
    for ( unsigned i=0; i<4; ++i ) out_Lepton_p4[i] = in_Electrons_p4[i]->At(leadElectronIdx);
  }
  else if ( mode_ == MODE::Auto ) {
    if ( leadMuonIdx != -1 ) {
      if ( vetoElectron1Idx != -1 ) return false;
      if      ( vetoMuon1Idx != -1 and vetoMuon1Idx != leadMuonIdx ) return false;
      else if ( vetoMuon2Idx != -1 and vetoMuon2Idx != leadMuonIdx ) return false;
      //out_Lepton_pdgId = -13*in_Muons_charge[leadMuonIdx];
      for ( unsigned i=0; i<4; ++i ) out_Lepton_p4[i] = in_Muons_p4[i]->At(leadMuonIdx);
    }
    else if ( leadElectronIdx != -1 ) {
      if ( vetoMuon1Idx != -1 ) return false;
      if      ( vetoElectron1Idx != -1 and vetoElectron1Idx != leadElectronIdx ) return false;
      else if ( vetoElectron2Idx != -1 and vetoElectron2Idx != leadElectronIdx ) return false;
      //out_Lepton_pdgId = -11*in_Electrons_charge->At(leadMuonIdx);
      for ( unsigned i=0; i<4; ++i ) out_Lepton_p4[i] = in_Electrons_p4[i]->At(leadElectronIdx);
    }
  }
  TLorentzVector leadLeptonP4;
  leadLeptonP4.SetPtEtaPhiM(out_Lepton_p4[0], out_Lepton_p4[1], out_Lepton_p4[2], out_Lepton_p4[3]);
  // Done for the leptons

  // Continue to the Jets
  std::vector<unsigned> jetIdxsByBDiscr;
  jetIdxsByBDiscr.reserve(in_Jets_bDiscr->GetSize());
  for ( int i=0, n=in_Jets_bDiscr->GetSize(); i<n; ++i ) {
    if ( !isGoodJet(i) ) continue;
    TLorentzVector jetP4 = buildP4(in_Jets_p4, i);
    if ( leadLeptonP4.DeltaR(jetP4) < 0.4 ) continue;
    jetIdxsByBDiscr.push_back(i);
  }
  if ( jetIdxsByBDiscr.size() < minEventNJets_ ) return false;

  // Sort jets by bDiscriminator
  std::sort(jetIdxsByBDiscr.begin(), jetIdxsByBDiscr.end(),
            [&](const unsigned i, const unsigned j){ return in_Jets_bDiscr->At(i) > in_Jets_bDiscr->At(j); });
  unsigned nBjets = 0;
  for ( auto i : jetIdxsByBDiscr ) {
    if ( in_Jets_bDiscr->At(i) > minBjetBDiscr_ ) ++nBjets;
  }
  if ( nBjets < minEventNBjets_ ) return false;

  // Now move to the next step to build W and top candidates
  if ( algo_ == ALGO::CloseMTop ) return reconstructTopByCloseMTop(out_MET_pt, out_MET_phi, leadLeptonP4, jetIdxsByBDiscr);

  return true;
}

bool ttbarSingleLeptonCppWorker::reconstructTopByCloseMTop(const double metPt, const double metPhi,
                                                           const TLorentzVector& leptonP4,
                                                           const std::vector<unsigned>& jetIdxs) {
  std::map<int, TLorentzVector> jetP4s;
  for ( auto i : jetIdxs ) jetP4s[i] = buildP4(in_Jets_p4, i);

  // Build hadronic side
  double bestDM = 1e9;
  int hadWJ1Idx = -1, hadWJ2Idx = -1, hadTJ0Idx = -1;
  for ( auto i : jetIdxs ) { // For the Jet1 from W
    for ( auto j : jetIdxs ) { // For the Jet2 from W
      if ( i <= j ) continue;
      const double mJJ = (jetP4s[i]+jetP4s[j]).M();
      for ( auto k : jetIdxs ) { // For the bjet from top
        if ( i == k or j == k ) continue;
        const double mJJJ = (jetP4s[i]+jetP4s[j]+jetP4s[k]).M();
        const double dM = std::abs(mJJ-mPDGW_)+std::abs(mJJJ-mPDGTop_);
        if ( bestDM > dM ) {
          hadWJ1Idx = i;
          hadWJ2Idx = j;
          hadTJ0Idx = k;
          bestDM = dM;
        }
      }
    }
  }
  if ( hadWJ1Idx == -1 or hadWJ2Idx == -1 or hadTJ0Idx == -1 ) return false;

  // Build leptonic side
  int lepJetIdx = -1;
  double minDphi = 1e9;
  TLorentzVector metP4;
  metP4.SetPtEtaPhiM(metPt, 0, metPhi, 0);
  const TLorentzVector lepWP4 = metP4+leptonP4;
  for ( int i=0, n=jetP4s.size(); i<n; ++i ) {
    if ( i == hadWJ1Idx or i == hadWJ2Idx or i == hadTJ0Idx ) continue;
    const double dPhi = lepWP4.DeltaPhi(jetP4s[i]);
    if ( dPhi < minDphi ) {
      minDphi = dPhi;
      lepJetIdx = i;
    }
  }
  if ( lepJetIdx == -1 ) return false;

  // Save results
  const TLorentzVector lepTP4 = leptonP4+metP4+jetP4s[lepJetIdx];
  const TLorentzVector hadWP4 = jetP4s[hadWJ1Idx]+jetP4s[hadWJ2Idx];
  const TLorentzVector hadTP4 = jetP4s[hadTJ0Idx]+hadWP4;

  out_LepW_p4[0] = lepWP4.Pt();
  out_LepW_p4[1] = lepWP4.Eta();
  out_LepW_p4[2] = lepWP4.Phi();
  out_LepW_p4[3] = lepWP4.M();

  out_LepT_p4[0] = lepTP4.Pt();
  out_LepT_p4[1] = lepTP4.Eta();
  out_LepT_p4[2] = lepTP4.Phi();
  out_LepT_p4[3] = lepTP4.M();

  out_HadW_p4[0] = hadWP4.Pt();
  out_HadW_p4[1] = hadWP4.Eta();
  out_HadW_p4[2] = hadWP4.Phi();
  out_HadW_p4[3] = hadWP4.M();

  out_HadT_p4[0] = hadTP4.Pt();
  out_HadT_p4[1] = hadTP4.Eta();
  out_HadT_p4[2] = hadTP4.Phi();
  out_HadT_p4[3] = hadTP4.M();

  out_LepTJ0_bDiscr = in_Jets_bDiscr->At(lepJetIdx);
  out_HadTJ0_bDiscr = in_Jets_bDiscr->At(hadTJ0Idx);
  out_HadWJ1_bDiscr = in_Jets_bDiscr->At(hadWJ1Idx);
  out_HadWJ2_bDiscr = in_Jets_bDiscr->At(hadWJ2Idx);

  out_LepTJ0_bDeepB = in_Jets_bDeepB->At(lepJetIdx);
  out_HadTJ0_bDeepB = in_Jets_bDeepB->At(hadTJ0Idx);
  out_HadWJ1_bDeepB = in_Jets_bDeepB->At(hadWJ1Idx);
  out_HadWJ2_bDeepB = in_Jets_bDeepB->At(hadWJ2Idx);

  out_LepTJ0_bDeepC = in_Jets_bDeepC->At(lepJetIdx);
  out_HadTJ0_bDeepC = in_Jets_bDeepC->At(hadTJ0Idx);
  out_HadWJ1_bDeepC = in_Jets_bDeepC->At(hadWJ1Idx);
  out_HadWJ2_bDeepC = in_Jets_bDeepC->At(hadWJ2Idx);

  out_nAddJets = 0;
  TLorentzVector addJets12[2];
  for ( auto jetIdx : jetIdxs ) {
    const int i = (int)jetIdx;
    if ( i == lepJetIdx ) continue;
    if ( i == hadWJ1Idx or i == hadWJ2Idx or i == hadTJ0Idx ) continue;

    for ( int j=0; j<4; ++j ) out_AddJets_p4[j][out_nAddJets] = in_Jets_p4[j]->At(jetIdx);
    out_AddJets_bDiscr[out_nAddJets] = in_Jets_bDiscr->At(jetIdx);
    out_AddJets_bDeepB[out_nAddJets] = in_Jets_bDeepB->At(jetIdx);
    out_AddJets_bDeepC[out_nAddJets] = in_Jets_bDeepC->At(jetIdx);
    ++out_nAddJets;
    if ( out_nAddJets <= 2 ) addJets12[out_nAddJets-1] = buildP4(in_Jets_p4, jetIdx);
    if ( out_nAddJets > nMaxAddJets_ ) break;
  }
  if ( out_nAddJets >= 2 ) {
    out_AddJets12_dR = addJets12[0].DeltaR(addJets12[1]);
    out_AddJets12_mass = (addJets12[0]+addJets12[1]).M();
  }

  return true;
}
