#ifndef PhysicsTools_ChickenChicken_FCNCTriLeptonCppWorker_H
#define PhysicsTools_ChickenChicken_FCNCTriLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class FCNCTriLeptonCppWorker {
//190306 KST 15:49 : just copy frome TTbarDouble~.h, changed class name
public:
  enum class MODE {Auto=0, ElElMu=111113, MuMuEl=131311, ElElEl=111111, MuMuMu=131313} mode_ = MODE::Auto;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;

  FCNCTriLeptonCppWorker(const std::string modeName, const std::string algoName);
  ~FCNCTriLeptonCppWorker() = default;

  void setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                TRAF relIso, TRAB isTight, isLoose, TRAB isGlobal, TRAB isPFcand, TRAB isTracker);
  void setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                    TRAF relIso, TRAI id, TRAI idTrig, TRAF dEtaSC, TRAF eCorr);
  void setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
               TRAI id, TRAF CSVv2);
  void setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi);

  void initOutput(TTree *outputTree);

  void resetValues();
  bool analyze();

private:
  //const double minLepton1Pt_ = 25, maxLepton1Eta_ = 2.4;
  //const double minLepton2Pt_ = 20, maxLepton2Eta_ = 2.4;

  const double minMuonPt_ = 30, maxMuonEta_ = 2.5; //Signal & veto reco. cuts are same
  const double minElectronPt_ = 35, maxElectronEta_ = 2.1; //Signal & veto reco. cuts are same
  const double minJetPt_ = 30, maxJetEta_ = 2.4;
  const double minGoodBjetBDiscr_ = 0.5426; // FIXME: give updated number (here, use Loose Working Point)
  const unsigned short minEventNGoodJets_ = 0, minEventNGoodBjets_ = 0;
  const double maxMuonRelIso_ = 0.15;
  const double maxVetoMuonRelIso_ = 0.25;

  bool isGoodMuon(const unsigned i) const;
  bool isGoodElectron(const unsigned i) const;
  bool isGoodJet(const unsigned i) const;

private:
  TLorentzVector buildP4(const TRAF p4Arr[], unsigned i) const;

private:
  TTreeReaderValue<float> *in_MET_pt = nullptr, *in_MET_phi = nullptr;
  TRAF in_Muons_p4[4];
  TRAI in_Muons_charge = nullptr;
  TRAF in_Muons_relIso = nullptr;
  TRAB in_Muons_isTight = nullptr;
  TRAB in_Muons_isLoose = nullptr; //veto muons
  TRAB in_Muons_isPFcand = nullptr;
  TRAB in_Muons_isGlobal = nullptr;
  TRAB in_Muons_isTracker = nullptr;//veto muons(isGlobal or isTracker)
  TRAF in_Electrons_p4[4];
  TRAI in_Electrons_charge = nullptr;
  TRAF in_Electrons_relIso = nullptr;
  TRAI in_Electrons_id = nullptr, in_Electrons_idTrg = nullptr;
  TRAF in_Electrons_dEtaSC = nullptr;
  TRAF in_Electrons_eCorr = nullptr;
  TRAF in_Jets_p4[4];
  TRAI in_Jets_id = nullptr;
  TRAF in_Jets_CSVv2 = nullptr;

private:
  bool _doCppOutput = false;

  float out_Lepton1_p4[4], out_Lepton2_p4[4], out_Lepton3_p4[4];
  int out_Lepton1_pdgId, out_Lepton2_pdgId, out_Lepton3_pdgId;
  float out_Z_p4[4];
  
  int out_Z_charge;

  float out_MET_pt, out_MET_phi;

  const static unsigned short maxNGoodJetsToKeep_ = 100;
  unsigned short out_nGoodJets, out_nGoodBjets;
  float out_Jets_p4[4][maxNGoodJetsToKeep_];
  float out_Jets_CSVv2[maxNGoodJetsToKeep_];

  unsigned short out_CutStep;

};

#endif
