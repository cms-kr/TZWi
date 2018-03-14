import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class partonTopEvent(Module, object):
    def __init__(self, *args, **kwargs):
        #super(partonTopEvent, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
        self.algo = kwargs.get("algo")

        if "/partonTop_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ partonTop worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/partonTopCppWorker.cc+O" % base)
            else:
                base = "%s/src/NanoCAT/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libNanoCATTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/partonTopCppWorker.h" % base)
        pass
    def beginJob(self):
        self.worker = ROOT.partonTopCppWorker()
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.worker.initOutput(wrappedOutputTree.tree())
        self.initReaders(inputTree)
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def initReaders(self,tree):

        objName = "GenPart"
        setattr(self, "n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "pdgId", "status", "genPartIdxMother"]:
            setattr(self, "%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        self.worker.setGenParticles(self.nGenPart,
                                    self.GenPart_pt, self.GenPart_eta, self.GenPart_phi, self.GenPart_mass,
                                    self.GenPart_pdgId, self.GenPart_status, self.GenPart_genPartIdxMother)
        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        return self.worker.genEvent()

partonTop = lambda : partonTopEvent()
