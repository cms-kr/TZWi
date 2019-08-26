import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TTbarDoubleLepton(Module, object):
    def __init__(self, *args, **kwargs):
        #super(TTbarDoubleLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
        self.eleIdName = kwargs.get("eleId") if "eleId" in kwargs else "cutBased"

        if "/TTbarDoubleLeptonCppWorker_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ TTbarDoubleLepton worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/TTbarDoubleLeptonCppWorker.cc+O" % base)
            else:
                base = "%s/src/TZWi/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libTZWiTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/TTbarDoubleLeptonCppWorker.h" % base)
        pass
    def beginJob(self):
        self.worker = ROOT.TTbarDoubleLeptonCppWorker(self.mode)
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for objName in ["Lepton1", "Lepton2", "Z"]:
            for varName in ["pt", "eta", "phi", "mass"]:
                self.out.branch("%s_%s" % (objName, varName), "F")
        self.out.branch("MET_pt", "F")
        self.out.branch("MET_phi", "F")
        self.out.branch("Lepton1_pdgId", "I")
        self.out.branch("Lepton2_pdgId", "I")
        self.out.branch("Z_charge", "I")
        #self.out.branch("nGoodJet", "i")
        self.out.branch("GoodJet_index", "i", lenVar="nGoodJet")
        for varName in ["pt", "eta", "phi", "mass", "CSVv2"]:
            self.out.branch("GoodJet_%s" % varName, "F", lenVar="nGoodJet")
        self.out.branch("nBjet", "i")

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
                        "pfRelIso03_all", self.eleIdName, "deltaEtaSC", "eCorr", "isPFcand"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Muon"
        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass", "charge",
                        "pfRelIso04_all", "tightId", "isGlobal", "isPFcand", "isTracker"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Jet"
        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
        for varName in ["pt", "eta", "phi", "mass",
                        "jetId", "puId", "btagCSVV2",]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        self.worker.setMET(self.b_MET_pt, self.b_MET_phi)
        self.worker.setElectrons(self.b_Electron_pt, self.b_Electron_eta, self.b_Electron_phi, self.b_Electron_mass, self.b_Electron_charge,
                                 self.b_Electron_pfRelIso03_all, getattr(self, "b_Electron_%s" % self.eleIdName),
                                 self.b_Electron_deltaEtaSC, self.b_Electron_eCorr, self.b_Electron_isPFcand)
        self.worker.setMuons(self.b_Muon_pt, self.b_Muon_eta, self.b_Muon_phi, self.b_Muon_mass, self.b_Muon_charge,
                             self.b_Muon_pfRelIso04_all,self.b_Muon_tightId, self.b_Muon_isGlobal, self.b_Muon_isPFcand, self.b_Muon_isTracker)
        self.worker.setJets(self.b_Jet_pt, self.b_Jet_eta, self.b_Jet_phi, self.b_Jet_mass,
                            self.b_Jet_jetId, self.b_Jet_btagCSVV2)
        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        self.worker.analyze()

        for objName in ["Lepton1", "Lepton2", "Z", "GoodJet"]:
            for varName in ["pt", "eta", "phi", "mass"]:
                setattr(event._tree, "b_out_%s_%s" % (objName, varName), getattr(self.worker, 'get_%s_%s' % (objName, varName))())
                self.out.fillBranch("%s_%s" % (objName, varName), getattr(event._tree, 'b_out_%s_%s' % (objName, varName)))
        for varName in ["MET_pt", "MET_phi", "Lepton1_pdgId", "Lepton2_pdgId", "Z_charge",
                        #"nGoodJet", ## We skip for this nGoodJet, which have to be done by the framework
                        "GoodJet_CSVv2", "GoodJet_index", "nBjet"]:
            setattr(event._tree, "b_out_%s" % (varName), getattr(self.worker, 'get_%s' % (varName))())
            self.out.fillBranch(varName, getattr(event._tree, "b_out_%s" % varName))
        ## Special care for nGoodJet, because we still want to use this variable from the next postproc.
        setattr(event._tree, "b_out_nGoodJet", self.worker.get_nGoodJet())

        return True

ttbar_DoubleLepton = lambda : TTbarDoubleLepton(mode="Auto")
ttbar_MuMu = lambda : TTbarDoubleLepton(mode="MuMu")
ttbar_ElEl = lambda : TTbarDoubleLepton(mode="ElEl")
ttbar_MuEl = lambda : TTbarDoubleLepton(mode="MuEl")
ttbar_MuMu_2016 = lambda : TTbarDoubleLepton(mode="MuMu", eleId="cutBased_Sum16")
ttbar_ElEl_2016 = lambda : TTbarDoubleLepton(mode="ElEl", eleId="cutBased_Sum16")
ttbar_MuEl_2016 = lambda : TTbarDoubleLepton(mode="MuEl", eleId="cutBased_Sum16")
