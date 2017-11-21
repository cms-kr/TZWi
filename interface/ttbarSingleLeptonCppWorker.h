#ifndef PhysicsTools_ChickenChicken_ttbarSingleLeptonCppWorker_H
#define PhysicsTools_ChickenChicken_ttbarSingleLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class ttbarSingleLeptonCppWorker {
public:
  enum class MODE {Auto=0, Electron=11, Muon=13} mode_ = MODE::Auto;
  enum class ALGO {
    CloseMTop=0,
  } algo_ = ALGO::CloseMTop;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;

  ttbarSingleLeptonCppWorker(const std::string modeName, const std::string algoName);
  ~ttbarSingleLeptonCppWorker();

  void setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                TRAF relIso, TRAB id);
  void setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                    TRAF relIso, TRAI id, TRAI idTrig, TRAF dEtaSC);
  void setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
               TRAI id, TRAF bDiscr, TRAF bDeepB, TRAF bDeepC);
  void setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi);

  void initOutput(TTree *outputTree);

  void resetValues();
  bool analyze();

private:
  const double minMuonPt_ = 30, maxMuonEta_ = 2.1;
  const double minElectronPt_ = 30, maxElectronEta_ = 2.1;
  const double minVetoMuonPt_ = 15, maxVetoMuonEta_ = 2.4;
  const double minVetoElectronPt_ = 15, maxVetoElectronEta_ = 2.4;
  const double minJetPt_ = 30, maxJetEta_ = 2.5;
  const double minBjetBDiscr_ = 0.5; // FIXME: give updated number
  const unsigned minEventNJets_ = 4, minEventNBjets_ = 2;

  bool isGoodMuon(const unsigned i) const;
  bool isVetoMuon(const unsigned i) const;
  bool isGoodElectron(const unsigned i) const;
  bool isVetoElectron(const unsigned i) const;
  bool isGoodJet(const unsigned i) const;

private:
  TLorentzVector buildP4(const TRAF p4Arr[], unsigned i) const;
  const double mPDGW_ = 80.4, mPDGTop_ = 172.5;
  bool reconstructTopByCloseMTop(const double metPt, const double metPhi,
                                 const TLorentzVector& leptonP4,
                                 const std::vector<unsigned>& jetIdxs); // reconstruct top quarks by choosing combinations closer to 80GeV/172.5GeV
private:
  TTreeReaderValue<float> *in_MET_pt = nullptr, *in_MET_phi = nullptr;
  TRAF in_Muons_p4[4];
  TRAI in_Muons_charge = nullptr;
  TRAF in_Muons_relIso = nullptr;
  TRAB in_Muons_id = nullptr;
  TRAF in_Electrons_p4[4];
  TRAI in_Electrons_charge = nullptr;
  TRAF in_Electrons_relIso = nullptr;
  TRAI in_Electrons_id = nullptr, in_Electrons_idTrg = nullptr;
  TRAF in_Electrons_dEtaSC = nullptr;
  TRAF in_Jets_p4[4];
  TRAI in_Jets_id = nullptr;
  TRAF in_Jets_bDiscr = nullptr;
  TRAF in_Jets_bDeepB = nullptr, in_Jets_bDeepC = nullptr;

private:
  bool _doCppOutput = false;

  float out_Lepton_p4[4];
  int out_Lepton_pdgId;

  float out_MET_pt, out_MET_phi;

  float out_LepT_p4[4], out_LepW_p4[4];
  float out_HadT_p4[4], out_HadW_p4[4];
  float out_LepTJ0_bDiscr, out_HadTJ0_bDiscr;
  float out_HadWJ1_bDiscr, out_HadWJ2_bDiscr;

  float out_LepTJ0_bDeepB, out_HadTJ0_bDeepB;
  float out_HadWJ1_bDeepB, out_HadWJ2_bDeepB;
  float out_LepTJ0_bDeepC, out_HadTJ0_bDeepC;
  float out_HadWJ1_bDeepC, out_HadWJ2_bDeepC;

  const static unsigned int nMaxAddJets_ = 100;
  unsigned out_nAddJets;
  float out_AddJets_p4[4][nMaxAddJets_];
  float out_AddJets_bDiscr[nMaxAddJets_];
  float out_AddJets_bDeepB[nMaxAddJets_];
  float out_AddJets_bDeepC[nMaxAddJets_];
  float out_AddJets12_dR, out_AddJets12_mass;

};

#endif
