import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.CombineHLT import CombineHLT

hlt_MuMu_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleMuon")
hlt_ElEl_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleEG")
hlt_MuEl_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.MuonEG")

hlt_MuMu_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleMuon")
hlt_ElEl_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleEG")
hlt_MuEl_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.MuonEG")

hlt_MuMu_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleMuon")
hlt_ElEl_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleEG")
hlt_MuEl_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.MuonEG")

hlt_MuMu_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleMuon")
hlt_ElEl_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleEG")
hlt_MuEl_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.MuonEG")

hlt_MuMu_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleMuon")
hlt_ElEl_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleEG")
hlt_MuEl_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.MuonEG")

hlt_MuMu_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleMuon")
hlt_ElEl_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleEG")
hlt_MuEl_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.MuonEG")

flags_MC2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="RunIISummer16")
flags_Run2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="Run2016")

flags_MC2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="RunIIFall17")
flags_Run2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="Run2017")
