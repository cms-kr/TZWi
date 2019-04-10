import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import sys

class CopyBranch(Module, object):
    def __init__(self, *args, **kwargs):
        self.brNames = []
        self.arrNames = {}
        if '--friend' not in sys.argv: return ## No need to run this module

        for brName in args[0]:
            if brName[-1] == ']': ## if this is given in an array
                brName1, brName2 = brName[:-1].split('[')
                if brName1 not in self.arrNames: self.arrNames[brName1] = brName2
                if brName2 not in self.brNames: self.brNames.append(brName2)
            else:
                if brName not in self.brNames: self.brNames.append(brName)
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
        self.arrNames, arrNames = {}, self.arrNames
        for br in [x for x in inputTree.GetListOfBranches() if x.GetName() in arrNames]:
            brName = br.GetName()
            self.out.branch(brName, typeNameMap[br.GetLeaf(brName).GetTypeName()], lenVar=arrNames[brName])
            self.arrNames[brName] = arrNames[brName]
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        for brName in self.brNames:
            self.out.fillBranch(brName, getattr(event, brName))
        for brName in self.arrNames:
            reader = getattr(event, brName)
            vals = [reader[i] for i in range(reader.GetSize())]
            self.out.fillBranch(brName, vals)
        return True

copyBranch = lambda: CopyBranch(["run", "event", "PV_npvsGood"])
copyMCBranch = lambda: CopyBranch(["genWeight", "LHEWeight_originalXWGTUP", "LHEPdfWeight[nLHEPdfWeight]",
                                   "LHEScaleWeight[nLHEScaleWeight]", "PSScaleWeight[nPSScaleWeight]"])

