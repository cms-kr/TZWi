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

hlt_E_Run2016  = lambda : CombineHLT(outName="HLT_E" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016.SingleElectron")
hlt_M_Run2016  = lambda : CombineHLT(outName="HLT_M" , fileName="fcncTriLepton/2016.yaml", hltSet="Run2016.SingleMuon")
hlt_MM_Run2016 = lambda : CombineHLT(outName="HLT_MM", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016.DoubleMuon")
hlt_EE_Run2016 = lambda : CombineHLT(outName="HLT_EE", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016.DoubleEG")
hlt_ME_Run2016 = lambda : CombineHLT(outName="HLT_ME", fileName="fcncTriLepton/2016.yaml", hltSet="Run2016.MuonEG")

flags_MC2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="RunIISummer16")
flags_Run2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="Run2016")

