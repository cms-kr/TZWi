#include "../interface/PartonTopCppWorker.h"
#include <iostream>
#include <cmath>

void PartonTopCppWorker::setGenParticles(TTreeReaderValue<unsigned> *nGenPart,
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

bool PartonTopCppWorker::hasSpecificAncestor(const unsigned i, const unsigned ancIdx) const {
  const int motherIdx = in_GenPart_genPartIdxMother->At(i);
  if ( motherIdx < 0 ) return false; // leached up to the root
  if ( motherIdx == int(ancIdx) ) return true;

  return hasSpecificAncestor(motherIdx, ancIdx);
}

int PartonTopCppWorker::findFirst(const int i) const {
  if ( i < 0 ) return -1; // for safety check
  const int motherIdx = in_GenPart_genPartIdxMother->At(i);
  if ( motherIdx < 0 ) return i; // already the first particle
  const int motherId = in_GenPart_pdgId->At(motherIdx);
  if ( motherId != in_GenPart_pdgId->At(i) ) return i;

  return findFirst(motherIdx);
}

void PartonTopCppWorker::resetValues() {
  out_pts.clear();
  out_etas.clear();
  out_phis.clear();
  out_masses.clear();
  out_pdgIds.clear();
  out_mothers.clear();
}

bool PartonTopCppWorker::genEvent(){
  using namespace std;

  resetValues();
  int nPartons = 0;
  const unsigned int nGenPart = **in_nGenPart;

  // Find top quarks
  std::set<unsigned> tQuarks, bosons;
  std::set<unsigned> leptons, taus, neutrinos, quarks;
  for ( unsigned i=0; i<nGenPart; ++i ) {
    const int aid = abs(in_GenPart_pdgId->At(i));
    if ( aid > 25 ) continue;
    const unsigned ii = findFirst(i);

    if ( std::abs(in_GenPart_eta->At(ii)) > 20 ) continue;

    if      ( aid == 6 ) tQuarks.insert(ii);
    else if ( aid >= 23 and aid <= 25 ) bosons.insert(ii);
    else if ( aid == 11 or aid == 13 ) leptons.insert(ii);
    else if ( aid == 15 ) taus.insert(ii);
    else if ( aid == 12 or aid == 14 or aid == 16 ) neutrinos.insert(ii);
    else if ( aid >= 1  and aid <= 5  ) quarks.insert(ii);
  }

  // Fill top quarks first
  std::map<unsigned, int> indexMap;
  for ( unsigned i : tQuarks ) {
    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(-1);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  // Continue to bosons. This might not be slow, but OK with just one or two top quarks in the event
  for ( unsigned i : bosons ) {
    int motherIdx = findFirst(in_GenPart_genPartIdxMother->At(i));
    if ( motherIdx >= 0 ) {
      auto match = indexMap.find(motherIdx);
      motherIdx = (match == indexMap.end()) ? -1 : match->second;
    }

    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(motherIdx);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  for ( unsigned i : quarks ) {
    int motherIdx = findFirst(in_GenPart_genPartIdxMother->At(i));
    if ( motherIdx >= 0 ) {
      auto match = indexMap.find(motherIdx);
      motherIdx = (match == indexMap.end()) ? -1 : match->second;
    }

    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(motherIdx);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  auto isFromBosons = [&](const unsigned i) {
    for ( unsigned j : bosons ) if ( hasSpecificAncestor(i, j) ) return true;
    return false;
  };

  for ( unsigned i : taus ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = findFirst(in_GenPart_genPartIdxMother->At(i));
    if ( motherIdx >= 0 ) {
      auto match = indexMap.find(motherIdx);
      motherIdx = (match == indexMap.end()) ? -1 : match->second;
    }

    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(motherIdx);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  for ( unsigned i : leptons ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = findFirst(in_GenPart_genPartIdxMother->At(i));
    if ( motherIdx >= 0 ) {
      auto match = indexMap.find(motherIdx);
      motherIdx = (match == indexMap.end()) ? -1 : match->second;
    }

    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(motherIdx);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  for ( unsigned i : neutrinos ) {
    if ( !isFromBosons(i) ) continue;
    int motherIdx = findFirst(in_GenPart_genPartIdxMother->At(i));
    if ( motherIdx >= 0 ) {
      auto match = indexMap.find(motherIdx);
      motherIdx = (match == indexMap.end()) ? -1 : match->second;
    }

    out_pts.push_back(in_GenPart_pt->At(i));
    out_etas.push_back(in_GenPart_eta->At(i));
    out_phis.push_back(in_GenPart_phi->At(i));
    out_masses.push_back(in_GenPart_mass->At(i));
    out_pdgIds.push_back(in_GenPart_pdgId->At(i));
    out_mothers.push_back(motherIdx);
    indexMap[i] = nPartons;
    ++nPartons;
  }

  return true;
}

