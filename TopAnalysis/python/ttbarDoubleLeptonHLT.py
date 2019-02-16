import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class CombineHLT(Module, object):
    def __init__(self, *args, **kwargs):
        #super(CombineHLT, self).__init__(*args, **kwargs)
        self.hltSetNames = kwargs.get("hltSets")
        self.outName = kwargs.get("outName") if "outName" in kwargs else "HLT"

        if "/CombineHLTCppWorker_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ CombineHLT worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/CombineHLTCppWorker.cc+O" % base)
            else:
                base = "%s/src/TZWi/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libTZWiTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/CombineHLTCppWorker.h" % base)

        pass
    def beginJob(self):
        self.worker = ROOT.CombineHLTCppWorker(self.outName)
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
        hltSets = {
            "MuonEG-MC_RunIISummer16":[
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
            ],
            "MuonEG-RD_Run2016BG":[
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
            ],
            "MuonEG-RD_Run2016H":[
                "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
                "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
            ],
            "DoubleMuon-MC_RunIISummer16":[
                "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",
                "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
                "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
                "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
            ],
            "DoubleMuon-RD_Run2016BG":[
                "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL",
                "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
            ],
            "DoubleMuon-RD_Run2016H":[
                "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
                "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",
            ],
            "DoubleEG-MC_RunIISummer16":[
                "HLT_Ele23_Ele12_CaloIdL_TrkIdL_IsoVL_DZ",
                "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
            ],
            "DoubleEG-RD_Run2016BG":[
                "HLT_Ele23_Ele12_CaloIdL_TrkIdL_IsoVL_DZ",
            ],
            "DoubleEG-RD_Run2016H":[
                "HLT_Ele23_Ele12_CaloIdL_TrkIdL_IsoVL_DZ",
            ],

            "Flags-MC_RunIISummer16":[
                "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
                "Flag_CSCTightHaloFilter", #"Flag_CSCTightHaloTrkMuUnvetoFilter",
                "Flag_HcalStripHaloFilter", "Flag_hcalLaserEventFilter",
                #"Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_EcalDeadCellBoundaryEnergyFilter",
                "Flag_goodVertices", "Flag_eeBadScFilter", #"Flag_ecalLaserCorrFilter",
                #"Flag_trkPOGFilters", "Flag_chargedHadronTrackResolutionFilter",
                "Flag_muonBadTrackFilter",
            ],
        }
        hltSets["Flags-RD_Run2016BG"] = hltSets["Flags-MC_RunIISummer16"][:]
        hltSets["Flags-RD_Run2016BG"].append("Flag_globalTightHalo2016Filter")
        #"Flag_globalSuperTightHalo2016Filter",
        hltSets["Flags-RD_Run2016H"] = hltSets["Flags-RD_Run2016BG"][:]

        for hltSetName in self.hltSetNames:
            for hltName in hltSets[hltSetName]:
                setattr(self, "b_"+hltName, tree.valueReader(hltName))
                self.worker.addHLT(getattr(self, "b_"+hltName))

        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        return self.worker.analyze()

ttbarHLT_MuMu_MC = lambda : CombineHLT(hltSets=["DoubleMuon-MC_RunIISummer16"])
ttbarHLT_ElEl_MC = lambda : CombineHLT(hltSets=["DoubleEG-MC_RunIISummer16"])
ttbarHLT_MuEl_MC = lambda : CombineHLT(hltSets=["MuonEG-MC_RunIISummer16"])

ttbarHLT_MuMu_Run2016BG = lambda : CombineHLT(hltSets=["DoubleMuon-RD_Run2016BG"])
ttbarHLT_ElEl_Run2016BG = lambda : CombineHLT(hltSets=["DoubleEG-RD_Run2016BG"])
ttbarHLT_MuEl_Run2016BG = lambda : CombineHLT(hltSets=["MuonEG-RD_Run2016BG"])

ttbarHLT_MuMu_Run2016H = lambda : CombineHLT(hltSets=["DoubleMuon-RD_Run2016H"])
ttbarHLT_ElEl_Run2016H = lambda : CombineHLT(hltSets=["DoubleEG-RD_Run2016H"])
ttbarHLT_MuEl_Run2016H = lambda : CombineHLT(hltSets=["MuonEG-RD_Run2016H"])

flags_MC = lambda : CombineHLT(outName="Flag", hltSets=["Flags-MC_RunIISummer16"])
flags_Run2016BG = lambda : CombineHLT(outName="Flag", hltSets=["Flags-RD_Run2016BG"])
flags_Run2016H = lambda : CombineHLT(outName="Flag", hltSets=["RD_Run2016H"])

