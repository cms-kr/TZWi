import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNHSingleLeptonCutFlow(Module, object):
    def __init__(self, *args, **kwargs):
        #super(FCNHSingleLepton, self).__init__(*args, **kwargs)
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
            if event._tree.b_out_Lepton1_pdgId == 0: break
            cutStep += 1
            if event._tree.b_out_nGoodJet >= 3: break
            cutStep += 1
            if event._tree.b_out_nBjet >= 1: break
            cutStep += 1
            if event._tree.b_out_nBjet >= 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return cutStep > 0

cutFlow_Mu = lambda: FCNHSingleLeptonCutFlow(mode="Mu")
cutFlow_El = lambda: FCNHSingleLeptonCutFlow(mode="El")
