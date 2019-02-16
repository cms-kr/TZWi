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

class CombineHLTCppWorker {
public:
  typedef TTreeReaderValue<bool>* TRB;

  CombineHLTCppWorker(const std::string outName="HLT");
  ~CombineHLTCppWorker() = default;

  void addHLT(TRB flag);
  void initOutput(TTree *outputTree);

  void resetValues();
  bool analyze();

private:
  std::vector<TRB> in_HLTFlags;

private:
  bool _doCppOutput = false;
  bool out_HLTFlag;
  const std::string outName_;

};

#endif
