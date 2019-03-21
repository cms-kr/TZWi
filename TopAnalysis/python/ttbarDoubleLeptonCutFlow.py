import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TTbarDoubleLeptonCutFlow(Module, object):
    def __init__(self, *args, **kwargs):
        #super(TTbarDoubleLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
        self.doMETCut = (self.mode != "MuEl")
        self.doZVetoCut = (self.mode != "MuEl")
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("CutStep", "i")

        self.initReaders(inputTree)
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def initReaders(self,tree):
        for name in ["Z_charge", "Z_mass", "Lepton1_pt", "Lepton2_pt", "MET_pt",
                     "nGoodJets", "nBjets"]:
            setattr(self, 'in_%s' % name, self.out._tree.GetBranch(name).GetLeaf(name))

        self._ttreereaderversion = tree._ttreereaderversion
        pass
    def analyze(self, event):
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)

        cutStep = 0
        while True:
            if self.in_Z_charge.GetValueLong64() != 0 or \
               self.in_Lepton1_pt.GetValue() < 25 or self.in_Lepton2_pt.GetValue() < 25: break
            cutStep += 1
            if self.doZVetoCut and (75 < self.in_Z_mass.GetValue() < 105): break
            cutStep += 1
            if self.doMETCut and self.in_MET_pt.GetValue() < 40: break
            cutStep += 1
            if self.in_nGoodJets.GetValueLong64() < 4: break
            cutStep += 1
            nBjets = self.in_nBjets.GetValueLong64()
            if nBjets < 1: break
            cutStep += 1
            if nBjets < 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return True

cutFlow_MuMu = lambda: TTbarDoubleLeptonCutFlow(mode="MuMu")
cutFlow_ElEl = lambda: TTbarDoubleLeptonCutFlow(mode="ElEl")
cutFlow_MuEl = lambda: TTbarDoubleLeptonCutFlow(mode="MuEl")
