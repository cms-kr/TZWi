#include "../interface/CombineHLTCppWorker.h"
#include <iostream>
#include <cmath>

using namespace std;

CombineHLTCppWorker::CombineHLTCppWorker(const std::string formulaExpr, const std::string outName):
  outName_(outName), formula_("", formulaExpr.c_str())
{
}

void CombineHLTCppWorker::initOutput(TTree *outputTree){
  if ( _doCppOutput ) return;

  //if (_doCppOutput) throw cms::Exception("LogicError","doCppOutput cannot be called twice");
  _doCppOutput = true;

  //outputTree->Branch(outName_.c_str(), &out_HLTFlag, (outName_+"/O").c_str());
  //outputTree->SetBranchAddress(outName_.c_str(), &out_HLTFlag);
  outputTree->GetBranch(outName_.c_str())->SetAddress(&out_HLTFlag);
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

  for ( int i=0; i<formula_.GetNpar(); ++i ) {
    formula_.SetParameter(i, static_cast<double>(**in_HLTFlags[i]));
  }

  return formula_.Eval(0);
}

