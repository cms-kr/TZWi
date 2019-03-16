#ifndef PhysicsTools_ChickenChicken_CombineHLTCppWorker_H
#define PhysicsTools_ChickenChicken_CombineHLTCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <array>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>
#include <TFormula.h>

class CombineHLTCppWorker {
public:
  typedef TTreeReaderValue<bool>* TRB;

  CombineHLTCppWorker(const std::string formulaExpr, const std::string outName="HLT");
  ~CombineHLTCppWorker() = default;

  void addHLT(TRB flag);
  bool analyze();

private:
  std::vector<TRB> in_HLTFlags;

private:
  const std::string outName_;
  TFormula formula_;

};

#endif
