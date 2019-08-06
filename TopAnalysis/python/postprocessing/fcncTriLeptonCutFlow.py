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

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        cutStep = 0
        while True:
            #if abs(event._tree.b_out_GoodLeptonCode) != 111: break
            if abs(event._tree.b_out_GoodLeptonCode) < 101: break
            cutStep += 1
            if event._tree.b_out_GoodLeptonCode < 0: break
            cutStep += 1
            if event._tree.b_out_nVetoLepton > 0: break
            cutStep += 1
            if not (1 <= event._tree.b_out_nGoodJet <= 3): break
            cutStep += 1
            if event._tree.b_out_W_MT > 300: break
            nBjet = event._tree.b_out_nBjet
            if nBjet < 1: break
            cutStep += 1
            if nBjet < 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return cutStep > 0

cutFlow_MuMuMu = lambda: FCNCTriLeptonCutFlow(mode="MuMuMu")
cutFlow_ElElEl = lambda: FCNCTriLeptonCutFlow(mode="ElElEl")
cutFlow_MuElEl = lambda: FCNCTriLeptonCutFlow(mode="MuElEl")
cutFlow_ElMuMu = lambda: FCNCTriLeptonCutFlow(mode="ElMuMu")
