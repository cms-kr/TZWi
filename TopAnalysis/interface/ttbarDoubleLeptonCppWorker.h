#ifndef PhysicsTools_ChickenChicken_ttbarDoubleLeptonCppWorker_H
#define PhysicsTools_ChickenChicken_ttbarDoubleLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class ttbarDoubleLeptonCppWorker {
public:
  enum class MODE {Auto=0, ElEl=1111, MuMu=1313, MuEl=1311} mode_ = MODE::Auto;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;

  ttbarDoubleLeptonCppWorker(const std::string modeName, const std::string algoName);
  ~ttbarDoubleLeptonCppWorker();

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
  const unsigned short minEventNJets_ = 0, minEventNBjets_ = 0;
  const double maxMuonRelIso_ = 0.15, maxVetoMuonRelIso_ = 0.20;

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

  float out_Lepton1_p4[4], out_Lepton2_p4[4];
  int out_Lepton1_pdgId, out_Lepton2_pdgId;
  float out_Z_p4[4];
  int out_Z_charge;

  float out_MET_pt, out_MET_phi;

  const static unsigned short maxNJetsToKeep_ = 100;
  unsigned short out_nJets, out_nBjets;
  float out_Jets_p4[4][maxNJetsToKeep_];
  float out_Jets_bDiscr[maxNJetsToKeep_];

};

#endif
