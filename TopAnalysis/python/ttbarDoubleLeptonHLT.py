import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.CombineHLT import CombineHLT

hlt_MuMu_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.DoubleMuon")
hlt_ElEl_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.DoubleEG")
hlt_MuEl_MC2016 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIISummer16.MuonEG")

hlt_MuMu_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.DoubleMuon")
hlt_ElEl_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.DoubleEG")
hlt_MuEl_MC2017 = lambda : CombineHLT(hltSet="ttbarDoubleLepton/MC_RunIIFall17.MuonEG")

hlt_MuMu_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.DoubleMuon")
hlt_ElEl_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.DoubleEG")
hlt_MuEl_Run2016BG = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016BG.MuonEG")

hlt_MuMu_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.DoubleMuon")
hlt_ElEl_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.DoubleEG")
hlt_MuEl_Run2016H = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2016H.MuonEG")

hlt_MuMu_Run2017B = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017B.DoubleMuon")
hlt_ElEl_Run2017B = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2017B.DoubleEG")
hlt_MuEl_Run2017B = lambda : CombineHLT(hltSet="ttbarDoubleLepton/RD_Run2017B.MuonEG")

hlt_MuMu_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.DoubleMuon")
hlt_ElEl_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.DoubleEG")
hlt_MuEl_Run2017CF = lambda : CombineHLT(hltset="ttbarDoubleLepton/RD_Run2017CF.MuonEG")

flags_MC2016 = lambda : CombineHLT(outName="Flag", hltSet="flags/MC_RunIISummer16.Flag")
flags_Run2016 = lambda : CombineHLT(outName="Flag", hltSet="flags/RD_Run2016.Flag")

flags_MC2017 = lambda : CombineHLT(outName="Flag", hltSet="flags/MC_RunIIFall17.Flag")
flags_Run2017 = lambda : CombineHLT(outName="Flag", hltSet="flags/RD_Run2017.Flag")
