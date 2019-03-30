import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

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

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        cutStep = 0
        while True:
            if event._tree.b_out_Z_charge != 0 or \
               event._tree.b_out_Lepton1_pt < 25 or event._tree.b_out_Lepton2_pt < 25: break
            cutStep += 1
            if self.doZVetoCut and ((75 < event._tree.b_out_Z_mass) and (event._tree.b_out_Z_mass < 105)): break
            cutStep += 1
            if self.doMETCut and event._tree.b_out_MET_pt < 40: break
            cutStep += 1
            if event._tree.b_out_nGoodJet < 4: break
            cutStep += 1
            nBjet = event._tree.b_out_nBjet
            if nBjet < 1: break
            cutStep += 1
            if nBjet < 2: break
            cutStep += 1

            break
        self.out.fillBranch("CutStep", cutStep)

        return (cutStep > 0)

cutFlow_MuMu = lambda: TTbarDoubleLeptonCutFlow(mode="MuMu")
cutFlow_ElEl = lambda: TTbarDoubleLeptonCutFlow(mode="ElEl")
cutFlow_MuEl = lambda: TTbarDoubleLeptonCutFlow(mode="MuEl")
