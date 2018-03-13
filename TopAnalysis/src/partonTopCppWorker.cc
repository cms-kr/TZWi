#include "../interface/partonTopCppWorker.h"
#include <iostream>
#include <cmath>

partonTopCppWorker::partonTopCppWorker(){
}

partonTopCppWorker::~partonTopCppWorker(){
}

void partonTopCppWorker::initOutput(TTree *outputTree){
  if ( _doCppOutput ) return;
  _doCppOutput = true;

  outputTree->Branch("nPartons", &out_nPartons, "nPartons/s");
  outputTree->Branch("Partons_pt"    , out_Partons_pt    , "Partons_pt[nPartons]/F"   );
  outputTree->Branch("Partons_eta"   , out_Partons_eta   , "Partons_eta[nPartons]/F"  );
  outputTree->Branch("Partons_phi"   , out_Partons_phi   , "Partons_phi[nPartons]/F"  );
  outputTree->Branch("Partons_mass"  , out_Partons_mass  , "Partons_mass[nPartons]/F"  );
  outputTree->Branch("Partons_pdgId" , out_Partons_pdgId , "Partons_pdgId[nPartons]/I" );
  outputTree->Branch("Partons_mother", out_Partons_mother, "Partons_mother[nPartons]/S");

}

void partonTopCppWorker::setGenParticles(TTreeReaderValue<unsigned> *nGenPart,
                                         TTreeReaderArray<float> *GenPart_pt, TTreeReaderArray<float> *GenPart_eta, TTreeReaderArray<float> *GenPart_phi, TTreeReaderArray<float> *GenPart_mass,
                                         TTreeReaderArray<int> *GenPart_pdgId, TTreeReaderArray<int> *GenPart_status,
                                         TTreeReaderArray<int> *GenPart_genPartIdxMother){
  in_nGenPart = nGenPart;  
  in_GenPart_pt = GenPart_pt;
  in_GenPart_eta = GenPart_eta;
  in_GenPart_phi = GenPart_phi;
  in_GenPart_mass = GenPart_mass;
  in_GenPart_pdgId = GenPart_pdgId;
  in_GenPart_status = GenPart_status;
  in_GenPart_genPartIdxMother = GenPart_genPartIdxMother;
}

bool partonTopCppWorker::hasSpecificAncestor(const unsigned i, const unsigned ancIdx) const {
  const int motherIdx = in_GenPart_genPartIdxMother->At(i);
  if ( motherIdx < 0 ) return false; // leached up to the root
  if ( motherIdx == int(ancIdx) ) return true;

  return hasSpecificAncestor(motherIdx, ancIdx);
}

int partonTopCppWorker::findFirst(const unsigned i) const {
  const int motherIdx = in_GenPart_genPartIdxMother->At(i);
  if ( motherIdx < 0 ) return i; // already the first particle
  const int motherId = in_GenPart_pdgId->At(motherIdx);
  if ( motherId != in_GenPart_pdgId->At(i) ) return i;

  return findFirst(motherIdx);
}

void partonTopCppWorker::resetValues() {
  out_nPartons = 0;
  for ( unsigned i=0; i<maxNPartons_; ++i ) {
    out_Partons_pt[i] = out_Partons_eta[i] = out_Partons_phi[i] = out_Partons_mass[i] = 0;
    out_Partons_pdgId[i] = out_Partons_mother[i] = 0;
  }
}

bool partonTopCppWorker::genEvent(){
  using namespace std;

  resetValues();
  const unsigned int nGenPart = **in_nGenPart;

  // Find top quarks
  std::set<unsigned> tQuarks, bosons;
  std::set<unsigned> leptons, taus, neutrinos, quarks;
  for ( unsigned i=0; i<nGenPart; ++i ) {
    const int aid = abs(in_GenPart_pdgId->At(i));
    if ( aid > 25 ) continue;

    if      ( aid == 6 ) tQuarks.insert(findFirst(i));
    else if ( aid >= 23 and aid <= 25 ) bosons.insert(findFirst(i));
    else if ( aid == 11 or aid == 13 ) leptons.insert(findFirst(i));
    else if ( aid == 15 ) taus.insert(findFirst(i));
    else if ( aid == 12 or aid == 14 or aid == 16 ) neutrinos.insert(findFirst(i));
    //else if ( aid >= 1  and aid <= 5  ) quarks.insert(findFirst(i));
  }

  // Fill top quarks first
  std::map<unsigned, int> indexMap;
  for ( unsigned i : tQuarks ) {
    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = -1;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  // Continue to bosons. This might not be slow, but OK with just one or two top quarks in the event
  for ( unsigned i : bosons ) {
    int motherIdx = in_GenPart_genPartIdxMother->At(i);
    if ( motherIdx >= 0 ) motherIdx = findFirst(motherIdx);
    auto match = indexMap.find(motherIdx);
    if ( match != indexMap.end() ) motherIdx = match->second;

    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = motherIdx;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  for ( unsigned i : quarks ) {
    int motherIdx = in_GenPart_genPartIdxMother->At(i);
    if ( motherIdx >= 0 ) motherIdx = findFirst(motherIdx);
    auto match = indexMap.find(motherIdx);
    if ( match != indexMap.end() ) motherIdx = match->second;

    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = motherIdx;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  auto isFromBosons = [&](const unsigned i) {
    for ( unsigned j : bosons ) if ( hasSpecificAncestor(i, j) ) return true;
    return false;
  };

  for ( unsigned i : taus ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = in_GenPart_genPartIdxMother->At(i);
    if ( motherIdx >= 0 ) motherIdx = findFirst(motherIdx);
    auto match = indexMap.find(motherIdx);
    if ( match != indexMap.end() ) motherIdx = match->second;

    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = motherIdx;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  for ( unsigned i : leptons ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = in_GenPart_genPartIdxMother->At(i);
    if ( motherIdx >= 0 ) motherIdx = findFirst(motherIdx);
    auto match = indexMap.find(motherIdx);
    if ( match != indexMap.end() ) motherIdx = match->second;

    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = motherIdx;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  for ( unsigned i : neutrinos ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = in_GenPart_genPartIdxMother->At(i);
    if ( motherIdx >= 0 ) motherIdx = findFirst(motherIdx);
    auto match = indexMap.find(motherIdx);
    if ( match != indexMap.end() ) motherIdx = match->second;

    out_Partons_pt[out_nPartons] = in_GenPart_pt->At(i);
    out_Partons_eta[out_nPartons] = in_GenPart_eta->At(i);
    out_Partons_phi[out_nPartons] = in_GenPart_phi->At(i);
    out_Partons_mass[out_nPartons] = in_GenPart_mass->At(i);
    out_Partons_pdgId[out_nPartons] = in_GenPart_pdgId->At(i);
    out_Partons_mother[out_nPartons] = motherIdx;
    indexMap[i] = out_nPartons;
    ++out_nPartons;
  }

  return true;
}

