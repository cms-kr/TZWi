#include "../interface/TTbarDoubleLeptonCppWorker.h"
#include <iostream>
#include <cmath>

using namespace std;

TTbarDoubleLeptonCppWorker::TTbarDoubleLeptonCppWorker(const std::string modeName, const std::string algoName)
{
  if      ( modeName == "Auto" ) mode_ = MODE::Auto;
  else if ( modeName == "ElEl" ) mode_ = MODE::ElEl;
  else if ( modeName == "MuMu" ) mode_ = MODE::MuMu;
  else if ( modeName == "MuEl" ) mode_ = MODE::MuEl;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. Fall back to \"Auto\"" << endl;
    mode_ = MODE::Auto;
  }

  cout << "AlgoName is dummy for now..." << algoName << endl;
}

void TTbarDoubleLeptonCppWorker::initOutput(TTree *outputTree){
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
    outputTree->Branch(Form("Z_%s", varNames[i].c_str()), &out_Z_p4[i], Form("Z_%s/F", varNames[i].c_str()));
  }
  outputTree->Branch("Z_charge", &out_Z_charge, "Z_charge/S");

  outputTree->Branch("MET_pt", &out_MET_pt, "MET_pt/F");
  outputTree->Branch("MET_phi", &out_MET_phi, "MET_phi/F");

  outputTree->Branch("nGoodJets", &out_nGoodJets, "nGoodJets/s");
  for ( unsigned i=0; i<4; ++i ) {
    outputTree->Branch(Form("Jets_%s", varNames[i].c_str()), out_Jets_p4[i], Form("Jets_%s[nGoodJets]/F", varNames[i].c_str()));
  }
  outputTree->Branch("Jets_CSVv2", out_Jets_CSVv2, "Jets_CSVv2[nGoodJets]/F");
  outputTree->Branch("nGoodBjets", &out_nGoodBjets, "nGoodBjets/s");

  outputTree->Branch("CutStep", &out_CutStep, "CutStep/s");
}

typedef TTbarDoubleLeptonCppWorker::TRAF TRAF;
typedef TTbarDoubleLeptonCppWorker::TRAI TRAI;
typedef TTbarDoubleLeptonCppWorker::TRAB TRAB;

void TTbarDoubleLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                                              TRAF relIso, TRAI id, TRAI idTrg, TRAF dEtaSC, TRAF eCorr) {
  in_Electrons_p4[0] = pt;
  in_Electrons_p4[1] = eta;
  in_Electrons_p4[2] = phi;
  in_Electrons_p4[3] = mass;
  in_Electrons_charge = charge;
  in_Electrons_relIso = relIso;
  in_Electrons_id = id;
  in_Electrons_idTrg = idTrg;
  in_Electrons_dEtaSC = dEtaSC;
  in_Electrons_eCorr = eCorr;
}

void TTbarDoubleLeptonCppWorker::setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
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

void TTbarDoubleLeptonCppWorker::setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
                                         TRAI id, TRAF CSVv2) {
  in_Jets_p4[0] = pt;
  in_Jets_p4[1] = eta;
  in_Jets_p4[2] = phi;
  in_Jets_p4[3] = mass;
  in_Jets_CSVv2 = CSVv2;
  in_Jets_id = id;
}

void TTbarDoubleLeptonCppWorker::setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi) {
  in_MET_pt = pt;
  in_MET_phi = phi;
}

void TTbarDoubleLeptonCppWorker::resetValues() {
  for ( unsigned i=0; i<4; ++i ) {
    out_Lepton1_p4[i] = out_Lepton2_p4[i] = 0;
  }
  out_Lepton1_pdgId = out_Lepton2_pdgId = 0;
  out_MET_pt = out_MET_phi = 0;
  out_nGoodJets = out_nGoodBjets = 0;
  for ( unsigned k=0; k<maxNGoodJetsToKeep_; ++k ) {
    for ( unsigned i=0; i<4; ++i ) out_Jets_p4[i][k] = 0;
  }
  out_CutStep = 0;
}

bool TTbarDoubleLeptonCppWorker::isGoodMuon(const unsigned i) const {
  const double pt = in_Muons_p4[0]->At(i);
  const double eta = in_Muons_p4[1]->At(i);
  if ( pt < minLepton2Pt_ or std::abs(eta) > maxLepton2Eta_ ) return false;
  //if ( in_Muons_isTight->At(i) == 0 ) return false;
  if ( ! (in_Muons_isPFcand->At(i) != 0 and (in_Muons_isGlobal->At(i) != 0 or in_Muons_isTracker->At(i) != 0)) ) return false;
  if ( in_Muons_relIso->At(i) < maxMuonRelIso_ ) return false;

  return true;
}

bool TTbarDoubleLeptonCppWorker::isGoodElectron(const unsigned i) const {
  const double pt = in_Electrons_p4[0]->At(i) * in_Electrons_eCorr->At(i);
  const double eta = in_Electrons_p4[1]->At(i);
  if ( pt < minLepton2Pt_ or std::abs(eta) > maxLepton2Eta_ ) return false;
  if ( in_Electrons_id->At(i) == 0 or in_Electrons_idTrg->At(i) == 0 ) return false;
  //if ( in_Electrons_relIso->At(i) < 0.15 ) return false; // Note: commented out since already applied in Cut based ID

  return true;
}

bool TTbarDoubleLeptonCppWorker::isGoodJet(const unsigned i) const {
  const double pt = in_Jets_p4[0]->At(i);
  const double eta = in_Jets_p4[1]->At(i);
  if ( pt < minJetPt_ or std::abs(eta) > maxJetEta_ ) return false;
  if ( in_Jets_id->At(i) == 0 ) return false;

  return true;
}

TLorentzVector TTbarDoubleLeptonCppWorker::buildP4(const TRAF p4Arr[], unsigned i) const {
  TLorentzVector p4;
  p4.SetPtEtaPhiM(p4Arr[0]->At(i), p4Arr[1]->At(i), p4Arr[2]->At(i), p4Arr[3]->At(i));
  return p4;
}

bool TTbarDoubleLeptonCppWorker::analyze() {
  resetValues();

  // Start from trivial stuffs
  out_MET_pt = **in_MET_pt;
  out_MET_phi = **in_MET_phi;

  // Select the two leading muons, keep veto muons as well up to 3
  int muon1Idx = -1, muon2Idx = -1;
  int nGoodMuons = 0;
  for ( unsigned i=0, n=in_Muons_p4[0]->GetSize(); i<n; ++i ) {
    const double pt = in_Muons_p4[0]->At(i);
    if ( isGoodMuon(i) ) {
      ++nGoodMuons;
      if ( muon2Idx < 0 or pt > in_Muons_p4[0]->At(muon2Idx) ) muon2Idx = i;
      if ( muon1Idx < 0 or pt > in_Muons_p4[0]->At(muon1Idx) ) std::swap(muon1Idx, muon2Idx);
    }
  }
  // Select the two leading electrons, keep veto electrons as well up to 3
  int electron1Idx = -1, electron2Idx = -1;
  int nGoodElectrons = 0;
  for ( unsigned i=0, n=in_Electrons_p4[0]->GetSize(); i<n; ++i ) {
    const double pt = in_Electrons_p4[0]->At(i) * in_Electrons_eCorr->At(i);
    if ( isGoodElectron(i) ) {
      ++nGoodElectrons;
      if ( electron2Idx < 0 or pt > in_Electrons_p4[0]->At(electron2Idx) * in_Electrons_eCorr->At(electron2Idx) ) electron2Idx = i;
      if ( electron1Idx < 0 or pt > in_Electrons_p4[0]->At(electron1Idx) * in_Electrons_eCorr->At(electron1Idx) ) std::swap(electron1Idx, electron2Idx);
    }
  }
  if ( nGoodMuons+nGoodElectrons < 2 ) return false; // Require at least two electrons.

  // Select event by decay mode
  auto actualMode = mode_;
  if ( mode_ == MODE::Auto ) {
    if      ( muon1Idx     == -1 or in_Muons_p4[0]->At(muon1Idx) < in_Electrons_p4[0]->At(electron2Idx) * in_Electrons_eCorr->At(electron2Idx) ) actualMode = MODE::ElEl;
    else if ( electron1Idx == -1 or in_Electrons_p4[0]->At(electron1Idx) *  in_Electrons_eCorr->At(electron1Idx) < in_Muons_p4[0]->At(muon2Idx) ) actualMode = MODE::MuMu;
    else actualMode = MODE::MuEl;
  }

  if ( actualMode == MODE::MuMu ) {
    if ( nGoodMuons < 2 ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Muons_p4[i]->At(muon1Idx);
      out_Lepton2_p4[i] = in_Muons_p4[i]->At(muon2Idx);
    }
    out_Lepton1_pdgId = -13*in_Muons_charge->At(muon1Idx);
    out_Lepton2_pdgId = -13*in_Muons_charge->At(muon2Idx);
  }
  else if ( actualMode == MODE::ElEl ) {
    if ( nGoodElectrons < 2 ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Electrons_p4[i]->At(electron1Idx) * in_Electrons_eCorr->At(electron1Idx);
      out_Lepton2_p4[i] = in_Electrons_p4[i]->At(electron2Idx) * in_Electrons_eCorr->At(electron2Idx);
    }
    out_Lepton1_pdgId = -11*in_Electrons_charge->At(electron1Idx);
    out_Lepton2_pdgId = -11*in_Electrons_charge->At(electron2Idx);
  }
  else if ( actualMode == MODE::MuEl ) {
    if ( nGoodMuons < 1 or nGoodElectrons < 1 ) return false;
    for ( unsigned i=0; i<4; ++i ) {
      out_Lepton1_p4[i] = in_Muons_p4[i]->At(muon1Idx);
      out_Lepton2_p4[i] = in_Electrons_p4[i]->At(electron1Idx) * in_Electrons_eCorr->At(electron1Idx);
    }
    out_Lepton1_pdgId = -13*in_Muons_charge->At(muon1Idx);
    out_Lepton2_pdgId = -11*in_Electrons_charge->At(electron1Idx);
  }
  if ( out_Lepton1_p4[0] < minLepton1Pt_ ) return false;

  TLorentzVector lepton1P4, lepton2P4;
  lepton1P4.SetPtEtaPhiM(out_Lepton1_p4[0], out_Lepton1_p4[1], out_Lepton1_p4[2], out_Lepton1_p4[3]);
  lepton2P4.SetPtEtaPhiM(out_Lepton2_p4[0], out_Lepton2_p4[1], out_Lepton2_p4[2], out_Lepton2_p4[3]);
  // Done for the leptons

  // Build Z candidate
  const auto zP4 = lepton1P4+lepton2P4;
  out_Z_p4[0] = zP4.Pt();
  out_Z_p4[1] = zP4.Eta();
  out_Z_p4[2] = zP4.Phi();
  out_Z_p4[3] = zP4.M();
  out_Z_charge = out_Lepton1_pdgId+out_Lepton2_pdgId;
  out_Z_charge = out_Z_charge == 0 ? 0 : 2*out_Z_charge/abs(out_Z_charge);

  // Continue to the Jets
  std::vector<unsigned short> jetIdxsByPt, jetIdxsByBDiscr;
  jetIdxsByPt.reserve(in_Jets_CSVv2->GetSize());
  jetIdxsByBDiscr.reserve(in_Jets_CSVv2->GetSize());
  for ( unsigned i=0, n=in_Jets_CSVv2->GetSize(); i<n; ++i ) {
    if ( !isGoodJet(i) ) continue;
    TLorentzVector jetP4 = buildP4(in_Jets_p4, i);
    if ( lepton1P4.DeltaR(jetP4) < 0.4 ) continue;
    if ( lepton2P4.DeltaR(jetP4) < 0.4 ) continue;
    jetIdxsByPt.push_back(i);
    jetIdxsByBDiscr.push_back(i);
    if ( in_Jets_CSVv2->At(i) > minGoodBjetBDiscr_ ) ++out_nGoodBjets;
  }
  out_nGoodJets = jetIdxsByPt.size();
  if ( out_nGoodJets < int(minEventNGoodJets_) ) return false;
  if ( out_nGoodBjets < int(minEventNGoodBjets_) ) return false;

  // Sort jets by CSVv2iminator
  std::sort(jetIdxsByPt.begin(), jetIdxsByPt.end(),
            [&](const unsigned short i, const unsigned short j){ return in_Jets_p4[0]->At(i) > in_Jets_p4[0]->At(j); });
  std::sort(jetIdxsByBDiscr.begin(), jetIdxsByBDiscr.end(),
            [&](const unsigned short i, const unsigned short j){ return in_Jets_CSVv2->At(i) > in_Jets_CSVv2->At(j); });
  for ( unsigned k=0, n=std::min(maxNGoodJetsToKeep_, out_nGoodJets); k<n; ++k ) {
    const unsigned kk = jetIdxsByBDiscr.at(k);
    for ( unsigned i=0; i<4; ++i ) out_Jets_p4[i][k] = in_Jets_p4[i]->At(kk);
    out_Jets_CSVv2[k] = in_Jets_CSVv2->At(kk);
  }

  // Get CutStep
  if ( actualMode == MODE::MuMu ) {
    if ( out_Z_charge == 0 and out_Lepton1_p4[0] > 25 and out_Lepton2_p4[0] > 20 ) {out_CutStep = 1;
      if ( out_Z_p4[0] < 75 or out_Z_p4[0] > 105 ) {out_CutStep = 2;
        if ( out_MET_pt > 40 ) {out_CutStep = 3;
          if ( out_nGoodJets > 3 ) {out_CutStep = 4;
            if ( out_nGoodBjets > 1 ) {out_CutStep = 5; 
            }
          }
        }
      }
    }
  }
  else if ( actualMode == MODE::ElEl ) {
   if ( out_Z_charge == 0 and out_Lepton1_p4[0] > 25 and out_Lepton2_p4[0] > 20 ) {out_CutStep = 1;
      if ( out_Z_p4[0] < 75 or out_Z_p4[0] > 105 ) {out_CutStep = 2;
        if ( out_MET_pt > 40 ) {out_CutStep = 3;
          if ( out_nGoodJets > 3 ) {out_CutStep = 4;
            if ( out_nGoodBjets > 1 ) {out_CutStep = 5;
            }
          }
        }
      }
    }
  }
  else if ( actualMode == MODE::MuEl ) {
   if ( out_Z_charge == 0 and out_Lepton1_p4[0] > 25 and out_Lepton2_p4[0] > 20 ) {out_CutStep = 3;
     if ( out_nGoodJets > 3 ) {out_CutStep = 4;
       if ( out_nGoodBjets > 1 ) {out_CutStep = 5;
        }  
      }
    }
  }

  return true;
}

