#ifndef PhysicsTools_ChickenChicken_FCNHSingleLeptonCppWorker_H
#define PhysicsTools_ChickenChicken_FCNHSingleLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class FCNHSingleLeptonCppWorker {
//190306 KST 15:49 : just copy frome TTbarDouble~.h, changed class name
public:
  enum class MODE {None=0, Mu=13, El=11} mode_ = MODE::None;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;

  FCNHSingleLeptonCppWorker(const std::string modeName);
  ~FCNHSingleLeptonCppWorker() = default;

  void setMuons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                TRAF relIso, TRAB isTight, TRAB isGlobal, TRAB isPFcand, TRAB isTracker);
  void setElectrons(TRAF pt, TRAF eta, TRAF phi, TRAF mass, TRAI charge,
                    TRAF relIso, TRAI id, TRAF dEtaSC, TRAF eCorr);
  void setJets(TRAF pt, TRAF eta, TRAF phi, TRAF mass,
               TRAI id, TRAF DeepCSV);
  void setMET(TTreeReaderValue<float>* pt, TTreeReaderValue<float>* phi);

  void resetValues();
  bool analyze();

  float get_Lepton1_pt()   const { return out_Lepton1_p4[0]; }
  float get_Lepton1_eta()  const { return out_Lepton1_p4[1]; }
  float get_Lepton1_phi()  const { return out_Lepton1_p4[2]; }
  float get_Lepton1_mass() const { return out_Lepton1_p4[3]; }
  int get_Lepton1_pdgId() const { return out_Lepton1_pdgId; }

  float get_MET_pt()  const { return out_MET_pt; }
  float get_MET_phi() const { return out_MET_phi; }

  unsigned get_nVetoLepton() const { return out_nVetoLepton; }
  unsigned get_nGoodJet()   const { return out_nGoodJet; }
  std::vector<float> get_GoodJet_pt()   const { return out_GoodJet_p4[0]; }
  std::vector<float> get_GoodJet_eta()  const { return out_GoodJet_p4[1]; }
  std::vector<float> get_GoodJet_phi()  const { return out_GoodJet_p4[2]; }
  std::vector<float> get_GoodJet_mass() const { return out_GoodJet_p4[3]; }
  std::vector<float> get_GoodJet_DeepCSV() const { return out_GoodJet_DeepCSV; }
  std::vector<unsigned short> get_GoodJet_index() const { return out_GoodJet_index; }
  unsigned get_nBjet()   const { return out_nBjet; }

private:
  const double minMuonPt_ = 30, maxMuonEta_ = 2.4; //Signal & veto reco. cuts are same
  const double minElectronPt_ = 30, maxElectronEta_ = 2.4; //Signal & veto reco. cuts are same
  const double minJetPt_ = 30, maxJetEta_ = 2.4;
  const double minBjetBDiscr_ = 0.4941; // give updated number - from constructor
  const double maxMuonRelIso_ = 0.15;
  const double maxVetoMuonRelIso_ = 0.25;

  bool isGoodMuon(const unsigned i) const;
  bool isVetoMuon(const unsigned i) const;
  bool isGoodElectron(const unsigned i) const;
  bool isVetoElectron(const unsigned i) const;
  bool isGoodJet(const unsigned i) const;

private:
  TLorentzVector buildP4(const TRAF p4Arr[], unsigned i) const;

private:
  TTreeReaderValue<float> *in_MET_pt = nullptr, *in_MET_phi = nullptr;
  TRAF in_Muons_p4[4];
  TRAI in_Muons_charge = nullptr;
  TRAF in_Muons_relIso = nullptr; //nanoAOD object : Muon_pfRelIso04_all
  TRAB in_Muons_isTight = nullptr;
  TRAB in_Muons_isLoose = nullptr; //veto muons
  TRAB in_Muons_isPFcand = nullptr;
  TRAB in_Muons_isGlobal = nullptr;
  TRAB in_Muons_isTracker = nullptr;//veto muons(isGlobal or isTracker)

  TRAF in_Electrons_p4[4];
  TRAI in_Electrons_charge = nullptr;
  TRAF in_Electrons_relIso = nullptr; //nanoAOD object : Electron_pfRelIso03_*
  TRAI in_Electrons_id = nullptr;
  TRAF in_Electrons_dEtaSC = nullptr;
  TRAF in_Electrons_eCorr = nullptr;

  TRAF in_Jet_p4[4];
  TRAI in_Jet_id = nullptr;
  TRAF in_Jet_DeepCSV = nullptr;

private:
  bool _doCppOutput = false;

  float out_Lepton1_p4[4];
  int out_Lepton1_pdgId;

  float out_MET_pt, out_MET_phi;

  unsigned short out_nVetoLepton;
  unsigned short out_nGoodJet, out_nBjet;
  std::vector<float> out_GoodJet_p4[4];
  std::vector<float> out_GoodJet_DeepCSV;
  std::vector<unsigned short> out_GoodJet_index;

};

#endif
