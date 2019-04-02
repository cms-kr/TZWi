import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import sys

class CopyBranch(Module, object):
    def __init__(self, *args, **kwargs):
        self.brNames = []
        if '--friend' not in sys.argv: return ## No need to run this module

        for bName in args[0]: self.brNames.append(bName)
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        typeNameMap = {'Float_t':'F', 'Double_t':'D', 'Int_t':'I', 'UInt_t':'i', 'Short_t':'S', 'UShort_t':'s',
                       'Long64_t':'L', 'ULong64_t':'l', 'Char_t':'C', 'UChar_t':'c'}
        self.brNames, brNames = [], self.brNames
        for br in [x for x in inputTree.GetListOfBranches() if x.GetName() in brNames]:
            brName = br.GetName()
            self.out.branch(brName, typeNameMap[br.GetLeaf(brName).GetTypeName()])
            self.brNames.append(brName)
            pass
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        for brName in self.brNames:
            self.out.fillBranch(brName, getattr(event, brName))
        return True

copyBranch = lambda: CopyBranch(["run", "event", "PV_npvsGood"])

