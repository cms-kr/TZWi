import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCTriLeptonCutFlow(Module, object):
    def __init__(self, *args, **kwargs):
        #super(FCNCTriLepton, self).__init__(*args, **kwargs)
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
        for name in ["W_MT", "nGoodJet", "nBjet"]:
            setattr(self, 'in_%s' % name, self.out._tree.GetBranch(name).GetLeaf(name))

        self._ttreereaderversion = tree._ttreereaderversion
        pass
    def analyze(self, event):
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)

        cutStep = 0
        while True:
            if not (1 <= self.in_nGoodJet.GetValueLong64() <= 3): break
            cutStep += 1
            if self.in_W_MT > 300: break
            nBjet = self.in_nBjet.GetValueLong64()
            if nBjet < 1: break
            cutStep += 1
            if nBjet < 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return True

cutFlow_MuMuMu = lambda: FCNCTriLeptonCutFlow(mode="MuMuMu")
cutFlow_ElElEl = lambda: FCNCTriLeptonCutFlow(mode="ElElEl")
cutFlow_ElElMu = lambda: FCNCTriLeptonCutFlow(mode="ElElMu")
cutFlow_MuMuEl = lambda: FCNCTriLeptonCutFlow(mode="MuMuEl")
