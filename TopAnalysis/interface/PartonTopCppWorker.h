#ifndef PhysicsTools_ChickenChicken_PartonTopCppWorker_H
#define PhysicsTools_ChickenChicken_PartonTopCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class PartonTopCppWorker {
public:
  PartonTopCppWorker();
  ~PartonTopCppWorker();

  void initOutput(TTree *outputTree);

  void resetValues();
  bool genEvent();

  void setGenParticles(TTreeReaderValue<unsigned> *nGenPart,
                       TTreeReaderArray<float> *GenPart_pt, TTreeReaderArray<float> *GenPart_eta, TTreeReaderArray<float> *GenPart_phi, TTreeReaderArray<float> *GenPart_mass,
                       TTreeReaderArray<int> *GenPart_pdgId, TTreeReaderArray<int> *GenPart_status,
                       TTreeReaderArray<int> *GenPart_genPartIdxMother);

private:
  bool hasSpecificAncestor(const unsigned i, const unsigned ancId) const;
  int findFirst(const int i) const;

private:
  TTreeReaderValue<unsigned> *in_nGenPart = nullptr;
  TTreeReaderArray<float> *in_GenPart_pt = nullptr;
  TTreeReaderArray<float> *in_GenPart_eta = nullptr;
  TTreeReaderArray<float> *in_GenPart_phi = nullptr;
  TTreeReaderArray<float> *in_GenPart_mass = nullptr;
  TTreeReaderArray<int> *in_GenPart_pdgId = nullptr;
  TTreeReaderArray<int> *in_GenPart_status = nullptr;
  TTreeReaderArray<int> *in_GenPart_genPartIdxMother = nullptr;

private:
  bool _doCppOutput = false;

  const unsigned static short maxNPartons_ = 100;
  unsigned short out_nPartons;
  float out_Partons_pt[maxNPartons_];
  float out_Partons_eta[maxNPartons_];
  float out_Partons_phi[maxNPartons_];
  float out_Partons_mass[maxNPartons_];
  int out_Partons_pdgId[maxNPartons_];
  short out_Partons_mother[maxNPartons_];

};

#endif
