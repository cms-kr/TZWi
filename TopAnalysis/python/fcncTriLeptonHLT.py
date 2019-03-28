import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.CombineHLT import CombineHLT

hlt_E_MC2016  = lambda : CombineHLT(outName="HLT_E" , fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16.SingleElectron")
hlt_M_MC2016  = lambda : CombineHLT(outName="HLT_M" , fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16.SingleMuon")
hlt_MM_MC2016 = lambda : CombineHLT(outName="HLT_MM", fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16.DoubleMuon")
hlt_EE_MC2016 = lambda : CombineHLT(outName="HLT_EE", fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16.DoubleEG")
hlt_ME_MC2016 = lambda : CombineHLT(outName="HLT_ME", fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16.MuonEG")

hlt_E_Run2016BE  = lambda : CombineHLT(outName="HLT_E" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.SingleElectron")
hlt_M_Run2016BE  = lambda : CombineHLT(outName="HLT_M" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.SingleMuon")
hlt_MM_Run2016BE = lambda : CombineHLT(outName="HLT_MM", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.DoubleMuon")
hlt_EE_Run2016BE = lambda : CombineHLT(outName="HLT_EE", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.DoubleEG")
hlt_ME_Run2016BE = lambda : CombineHLT(outName="HLT_ME", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.MuonEG")

hlt_E_Run2016FG  = lambda : CombineHLT(outName="HLT_E" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.SingleElectron")
hlt_M_Run2016FG  = lambda : CombineHLT(outName="HLT_M" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.SingleMuon")
hlt_MM_Run2016FG = lambda : CombineHLT(outName="HLT_MM", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.DoubleMuon")
hlt_EE_Run2016FG = lambda : CombineHLT(outName="HLT_EE", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.DoubleEG")
hlt_ME_Run2016FG = lambda : CombineHLT(outName="HLT_ME", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.MuonEG")

hlt_E_Run2016H  = lambda : CombineHLT(outName="HLT_E" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.SingleElectron")
hlt_M_Run2016H  = lambda : CombineHLT(outName="HLT_M" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.SingleMuon")
hlt_MM_Run2016H = lambda : CombineHLT(outName="HLT_MM", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.DoubleMuon")
hlt_EE_Run2016H = lambda : CombineHLT(outName="HLT_EE", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.DoubleEG")
hlt_ME_Run2016H = lambda : CombineHLT(outName="HLT_ME", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.MuonEG")

flags_MC2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="RunIISummer16")
flags_Run2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="Run2016")

