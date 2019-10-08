import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCTriLepton(Module, object):
    def __init__(self, *args, **kwargs):
        #super(FCNCTriLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
        self.eleIdName = kwargs.get("eleId") if "eleId" in kwargs else "cutBased"

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
        self.out = wrappedOutputTree
        for objName in ["Lepton1", "Lepton2", "Lepton3", "Z", "LeadingElectron", "LeadingMuon"]:
            for varName in ["pt", "eta", "phi", "mass"]:
                self.out.branch("%s_%s" % (objName, varName), "F")
        self.out.branch("MET_pt", "F")
        self.out.branch("MET_phi", "F")
        self.out.branch("Lepton1_pdgId", "I")
        self.out.branch("Lepton2_pdgId", "I")
        self.out.branch("Lepton3_pdgId", "I")
        self.out.branch("LeptonTotal_mass", "F")
        self.out.branch("LeptonTotal_pt", "F")
        self.out.branch("LeptonWandZ_deltaPhi", "F")
        self.out.branch("LeptonWandZ_deltaR", "F")
        self.out.branch("Z_charge", "I")
        self.out.branch("nVetoLepton", "i")
        self.out.branch("GoodLeptonCode", "I")
        #self.out.branch("nGoodJet", "i")
        self.out.branch("GoodJet_index", "i", lenVar="nGoodJet")
        for varName in ["pt", "eta", "phi", "mass", "CSVv2"]:
            self.out.branch("GoodJet_%s" % varName, "F", lenVar="nGoodJet")
        self.out.branch("nBjet", "i")
        self.out.branch("W_MT", "F")

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
                        "pfRelIso03_all", self.eleIdName, "deltaEtaSC", "eCorr",]:
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
                                 self.b_Electron_pfRelIso03_all, getattr(self, 'b_Electron_%s' % self.eleIdName),
                                 self.b_Electron_deltaEtaSC, self.b_Electron_eCorr)
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

        for objName in ["Lepton1", "Lepton2", "Lepton3", "Z", "GoodJet", "LeadingElectron", "LeadingMuon"]:
            for varName in ["pt", "eta", "phi", "mass"]:
                setattr(event._tree, "b_out_%s_%s" % (objName, varName), getattr(self.worker, 'get_%s_%s' % (objName, varName))())
                self.out.fillBranch("%s_%s" % (objName, varName), getattr(event._tree, 'b_out_%s_%s' % (objName, varName)))
        for varName in ["MET_pt", "MET_phi", "Lepton1_pdgId", "Lepton2_pdgId", "Lepton3_pdgId",
                        "LeptonTotal_mass", "LeptonTotal_pt", "LeptonWandZ_deltaPhi", "LeptonWandZ_deltaR",
                        "nVetoLepton", "GoodLeptonCode", "Z_charge", "W_MT",
                        #"nGoodJet", #We do not keep nGoodJet here, it have to be done by the framework
                        "GoodJet_index", "GoodJet_CSVv2",
                        "nBjet",]:
            setattr(event._tree, "b_out_%s" % (varName), getattr(self.worker, 'get_%s' % (varName))())
            self.out.fillBranch(varName, getattr(event._tree, "b_out_%s" % varName))
        ## Special care for nGoodJet
        setattr(event._tree, "b_out_nGoodJet", self.worker.get_nGoodJet())

        return True

fcnc_MuMuMu_2016 = lambda : FCNCTriLepton(mode="MuMuMu", eleId="cutBased_Sum16")
fcnc_ElElEl_2016 = lambda : FCNCTriLepton(mode="ElElEl", eleId="cutBased_Sum16")
fcnc_ElMuMu_2016 = lambda : FCNCTriLepton(mode="ElMuMu", eleId="cutBased_Sum16")
fcnc_MuElEl_2016 = lambda : FCNCTriLepton(mode="MuElEl", eleId="cutBased_Sum16")

fcnc_MuMuMu_2017 = lambda : FCNCTriLepton(mode="MuMuMu", eleId="cutBased_Fall17_V1")
fcnc_ElElEl_2017 = lambda : FCNCTriLepton(mode="ElElEl", eleId="cutBased_Fall17_V1")
fcnc_ElMuMu_2017 = lambda : FCNCTriLepton(mode="ElMuMu", eleId="cutBased_Fall17_V1")
fcnc_MuElEl_2017 = lambda : FCNCTriLepton(mode="MuElEl", eleId="cutBased_Fall17_V1")
