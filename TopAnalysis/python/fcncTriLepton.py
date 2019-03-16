import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCTriLepton(Module, object):
    def __init__(self, *args, **kwargs):
        #super(FCNCTriLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")

        if "/FCNCTriLeptonCppWorker_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ FCNCTriLepton worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/FCNCTriLeptonCppWorker.cc+O" % base)
            else:
                base = "%s/src/TZWi/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libTZWiTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/FCNCTriLeptonCppWorker.h" % base)
        pass
    def beginJob(self):
        self.worker = ROOT.FCNCTriLeptonCppWorker(self.mode)
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

        self.b_MET_pt = tree.valueReader("MET_pt")
        self.b_MET_phi = tree.valueReader("MET_phi")

        objName = "Electron"
        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "charge",
                        "pfRelIso03_all", "cutBased", "deltaEtaSC", "eCorr",]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Muon"
        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "charge",
                        "pfRelIso04_all", "tightId", "globalMu", "isPFcand", "trackerMu"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Jet"
        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass",
                        "jetId", "puId", "btagCSVV2",]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        self.worker.setMET(self.b_MET_pt, self.b_MET_phi)
        self.worker.setElectrons(self.b_Electron_pt, self.b_Electron_eta, self.b_Electron_phi, self.b_Electron_mass, self.b_Electron_charge,
                                 self.b_Electron_pfRelIso03_all, self.b_Electron_cutBased, self.b_Electron_cutBased_HLTPreSel,
                                 self.b_Electron_deltaEtaSC, self.b_Electron_eCorr)
        self.worker.setMuons(self.b_Muon_pt, self.b_Muon_eta, self.b_Muon_phi, self.b_Muon_mass, self.b_Muon_charge,
                             self.b_Muon_pfRelIso04_all,self.b_Muon_tightId, self.b_Muon_globalMu, self.b_Muon_isPFcand, self.b_Muon_trackerMu)
        self.worker.setJets(self.b_Jet_pt, self.b_Jet_eta, self.b_Jet_phi, self.b_Jet_mass,
                            self.b_Jet_jetId, self.b_Jet_btagCSVV2)
        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        return self.worker.analyze()

fcncMuMuMu = lambda : FCNCTriLepton(mode="MuMuMu")
fcncElElEl = lambda : FCNCTriLepton(mode="ElElEl")
fcncMuMuEl = lambda : FCNCTriLepton(mode="MuMuEl")
fcncElElMu = lambda : FCNCTriLepton(mode="ElElMu")
