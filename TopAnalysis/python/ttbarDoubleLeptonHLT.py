import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.CombineHLT import CombineHLT

ttbarHLT_MuMu_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.DoubleMuon")
ttbarHLT_ElEl_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.DoubleEG")
ttbarHLT_MuEl_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.MuonEG")

ttbarHLT_MuMu_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.DoubleMuon")
ttbarHLT_ElEl_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.DoubleEG")
ttbarHLT_MuEl_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.MuonEG")

ttbarHLT_MuMu_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.DoubleMuon")
ttbarHLT_ElEl_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.DoubleEG")
ttbarHLT_MuEl_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.MuonEG")

ttbarHLT_MuMu_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.DoubleMuon")
ttbarHLT_ElEl_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.DoubleEG")
ttbarHLT_MuEl_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.MuonEG")

ttbarHLT_MuMu_Run2017B = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017B.DoubleMuon")
ttbarHLT_ElEl_Run2017B = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2017B.DoubleEG")
ttbarHLT_MuEl_Run2017B = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2017B.MuonEG")

ttbarHLT_MuMu_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.DoubleMuon")
ttbarHLT_ElEl_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.DoubleEG")
ttbarHLT_MuEl_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.MuonEG")

flags_MC2016 = lambda : CombineHLT(outName="Flag", hltSet="flags/MC_RunIISummer16.Flag")
flags_Run2016 = lambda : CombineHLT(outName="Flag", hltSet="flags/RD_Run2016.Flag")

flags_MC2017 = lambda : CombineHLT(outName="Flag", hltSet="flags/MC_RunIIFall17.Flag")
flags_Run2017 = lambda : CombineHLT(outName="Flag", hltSet="flags/RD_Run2017.Flag")
