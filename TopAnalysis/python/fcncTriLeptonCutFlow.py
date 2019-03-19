import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TTbarDoubleLeptonCutFlow(Module, object):
    def __init__(self, *args, **kwargs):
        #super(TTbarDoubleLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
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
        for name in ["W_MT", "nGoodJets", "nBjets"]:
            setattr(self, 'in_%s' % name, self.out._tree.GetBranch(name).GetLeaf(name))

        self._ttreereaderversion = tree._ttreereaderversion
        pass
    def analyze(self, event):
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)

        cutStep = 0
        while True:
            if not (1 <= self.in_nGoodJets.GetValueLong64() <= 3): break
            cutStep += 1
            if self.in_W_MT > 300: break
            nBjets = self.in_nBjets.GetValueLong64()
            if nBjets < 1: break
            cutStep += 1
            if nBjets < 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return True

cutFlow_MuMuMu = lambda: TTbarDoubleLeptonCutFlow(mode="MuMuMu")
cutFlow_ElElEl = lambda: TTbarDoubleLeptonCutFlow(mode="ElElEl")
cutFlow_MuElEl = lambda: TTbarDoubleLeptonCutFlow(mode="MuElEl")
cutFlow_ElMuMu = lambda: TTbarDoubleLeptonCutFlow(mode="ElMuMu")
