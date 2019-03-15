#include "../interface/CombineHLTCppWorker.h"
#include <iostream>
#include <cmath>

using namespace std;

CombineHLTCppWorker::CombineHLTCppWorker(const std::string formulaExpr, const std::string outName):
  outName_(outName), formula_(("CombineHLT_"+outName).c_str(), formulaExpr.c_str())
{
}

typedef CombineHLTCppWorker::TRB TRB;

void CombineHLTCppWorker::addHLT(TRB HLTFlag) {
  in_HLTFlags.push_back(HLTFlag);
}

bool CombineHLTCppWorker::analyze() {
  for ( int i=0; i<formula_.GetNpar(); ++i ) {
    formula_.SetParameter(i, static_cast<double>(**in_HLTFlags[i]));
  }

  return formula_.Eval(0);
}

