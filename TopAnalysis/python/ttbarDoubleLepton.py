import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ttbarDoubleLeptonEvent(Module, object):
    def __init__(self, *args, **kwargs):
        #super(ttbarDoubleLeptonEvent, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
        self.algo = kwargs.get("algo")

        if "/ttbarDoubleLepton_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ ttbarDoubleLepton worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/ttbarDoubleLeptonCppWorker.cc+O" % base)
            else:
                base = "%s/src/TZWi/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libTZWiTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/ttbarDoubleLeptonCppWorker.h" % base)
        pass
    def beginJob(self):
        self.worker = ROOT.ttbarDoubleLeptonCppWorker(self.mode, self.algo)
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

        self.MET_pt = tree.valueReader("MET_pt")
        self.MET_phi = tree.valueReader("MET_phi")

        objName = "Electron"
        setattr(self, "n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "charge",
                        "pfRelIso03_all", "cutBased", "cutBased_HLTPreSel", "deltaEtaSC", "eCorr",]:
            setattr(self, "%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Muon"
        setattr(self, "n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "charge",
                        "pfRelIso04_all", "tightId", "globalMu", "isPFcand", "trackerMu"]:
            setattr(self, "%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Jet"
        setattr(self, "n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass",
                        "jetId", "puId", "btagCSVV2",]:
            setattr(self, "%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        self.worker.setMET(self.MET_pt, self.MET_phi)
        self.worker.setElectrons(self.Electron_pt, self.Electron_eta, self.Electron_phi, self.Electron_mass, self.Electron_charge,
                                 self.Electron_pfRelIso03_all, self.Electron_cutBased, self.Electron_cutBased_HLTPreSel, self.Electron_deltaEtaSC, self.Electron_eCorr)
        self.worker.setMuons(self.Muon_pt, self.Muon_eta, self.Muon_phi, self.Muon_mass, self.Muon_charge,
                             self.Muon_pfRelIso04_all,self.Muon_tightId, self.Muon_globalMu, self.Muon_isPFcand, self.Muon_trackerMu)
        self.worker.setJets(self.Jet_pt, self.Jet_eta, self.Jet_phi, self.Jet_mass,
                            self.Jet_jetId, self.Jet_btagCSVV2)
        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        return self.worker.analyze()

ttbarDoubleLepton = lambda : ttbarDoubleLeptonEvent(mode="Auto", algo="Auto")
