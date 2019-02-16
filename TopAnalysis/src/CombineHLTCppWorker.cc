#include "../interface/CombineHLTCppWorker.h"
#include <iostream>
#include <cmath>

using namespace std;

CombineHLTCppWorker::CombineHLTCppWorker(const std::string outName): outName_(outName) {
}

void CombineHLTCppWorker::initOutput(TTree *outputTree){
  if ( _doCppOutput ) return;

  //if (_doCppOutput) throw cms::Exception("LogicError","doCppOutput cannot be called twice");
  _doCppOutput = true;

  outputTree->Branch(outName_.c_str(), &out_HLTFlag, (outName_+"/O").c_str());
}

typedef CombineHLTCppWorker::TRB TRB;

void CombineHLTCppWorker::addHLT(TRB HLTFlag) {
  in_HLTFlags.push_back(HLTFlag);
}

void CombineHLTCppWorker::resetValues() {
  out_HLTFlag = false;
}

bool CombineHLTCppWorker::analyze() {
  resetValues();

  for ( auto& in_HLTFlag : in_HLTFlags ) {
    if ( **in_HLTFlag == true ) {
      out_HLTFlag = true;
      break;
    }
  }

  return true;
}

