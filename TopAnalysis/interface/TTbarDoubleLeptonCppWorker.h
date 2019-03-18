#ifndef PhysicsTools_ChickenChicken_TTbarDoubleLeptonCppWorker_H
#define PhysicsTools_ChickenChicken_TTbarDoubleLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class TTbarDoubleLeptonCppWorker {
public:
  enum class MODE {Auto=0, ElEl=1111, MuMu=1313, MuEl=1311} mode_ = MODE::Auto;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;

  TTbarDoubleLeptonCppWorker(const std::string modeName, const std::string algoName);
  ~TTbarDoubleLeptonCppWorker() = default;

  void setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                TRAF relIso, TRAB isTight, TRAB isGlobal, TRAB isPFcand, TRAB isTracker);
  void setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                    TRAF relIso, TRAI id, TRAI idTrig, TRAF dEtaSC);
  void setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
               TRAI id, TRAF CSVv2);
  void setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi);

  void initOutput(TTree *outputTree);

  void resetValues();
  bool analyze();

  float get_Lepton1_pt()   const { return out_Lepton1_p4[0]; }
  float get_Lepton1_eta()  const { return out_Lepton1_p4[1]; }
  float get_Lepton1_phi()  const { return out_Lepton1_p4[2]; }
  float get_Lepton1_mass() const { return out_Lepton1_p4[3]; }
  int get_Lepton1_pdgId() const { return out_Lepton1_pdgId; }

  float get_Lepton2_pt()   const { return out_Lepton2_p4[0]; }
  float get_Lepton2_eta()  const { return out_Lepton2_p4[1]; }
  float get_Lepton2_phi()  const { return out_Lepton2_p4[2]; }
  float get_Lepton2_mass() const { return out_Lepton2_p4[3]; }
  int get_Lepton2_pdgId() const { return out_Lepton2_pdgId; }

  float get_Z_pt()   const { return out_Z_p4[0]; }
  float get_Z_eta()  const { return out_Z_p4[1]; }
  float get_Z_phi()  const { return out_Z_p4[2]; }
  float get_Z_mass() const { return out_Z_p4[3]; }
  int get_Z_charge() const { return out_Z_charge; }

  float get_MET_pt() const { return out_MET_pt; }
  float get_MET_phi() const { return out_MET_phi; }

  unsigned get_nGoodJets() const { return out_nGoodJets; }
  std::vector<float> get_GoodJets_pt()   const { return out_Jets_p4[0]; }
  std::vector<float> get_GoodJets_eta()  const { return out_Jets_p4[1]; }
  std::vector<float> get_GoodJets_phi()  const { return out_Jets_p4[2]; }
  std::vector<float> get_GoodJets_mass() const { return out_Jets_p4[3]; }
  std::vector<float> get_GoodJets_CSVv2() const { return out_Jets_CSVv2; }

  unsigned get_nBjets() const { return out_nBjets; }

private:
  const double minLepton1Pt_ = 25, maxLepton1Eta_ = 2.4;
  const double minLepton2Pt_ = 20, maxLepton2Eta_ = 2.4;
  const double minJetPt_ = 30, maxJetEta_ = 2.5;
  const double minBjetBDiscr_ = 0.8484; // FIXME: give updated number
  const unsigned short minEventNGoodJets_ = 0, minEventNBjets_ = 0;
  const double maxMuonRelIso_ = 0.15;

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
  TRAB in_Muons_isPFcand = nullptr;
  TRAB in_Muons_isGlobal = nullptr;
  TRAB in_Muons_isTracker = nullptr;
  TRAF in_Electrons_p4[4];
  TRAI in_Electrons_charge = nullptr;
  TRAF in_Electrons_relIso = nullptr;
  TRAI in_Electrons_id = nullptr, in_Electrons_idTrg = nullptr;
  TRAF in_Electrons_dEtaSC = nullptr;
  //TRAF in_Electrons_eCorr = nullptr;
  TRAF in_Jets_p4[4];
  TRAI in_Jets_id = nullptr;
  TRAF in_Jets_CSVv2 = nullptr;

private:
  bool _doCppOutput = false;

  float out_Lepton1_p4[4], out_Lepton2_p4[4];
  int out_Lepton1_pdgId, out_Lepton2_pdgId;
  float out_Z_p4[4];
  int out_Z_charge;

  float out_MET_pt, out_MET_phi;

  const static unsigned short maxNGoodJetsToKeep_ = 100;
  unsigned short out_nGoodJets, out_nBjets;
  std::vector<float> out_Jets_p4[4];
  std::vector<float> out_Jets_CSVv2;

  unsigned short out_CutStep;

};

#endif
