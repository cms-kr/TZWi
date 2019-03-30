import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

hlt_MuMu_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleMuon", doFilter=True)
hlt_ElEl_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleEG", doFilter=True)
hlt_MuEl_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.MuonEG", doFilter=True)

hlt_MuMu_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleMuon", doFilter=True)
hlt_ElEl_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleEG", doFilter=True)
hlt_MuEl_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.MuonEG", doFilter=True)

hlt_MuMu_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleMuon", doFilter=True)
hlt_ElEl_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleEG", doFilter=True)
hlt_MuEl_Run2016BG = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.MuonEG", doFilter=True)

hlt_MuMu_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleMuon", doFilter=True)
hlt_ElEl_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleEG", doFilter=True)
hlt_MuEl_Run2016H = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.MuonEG", doFilter=True)

hlt_MuMu_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleMuon", doFilter=True)
hlt_ElEl_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleEG", doFilter=True)
hlt_MuEl_Run2017B = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.MuonEG", doFilter=True)

hlt_MuMu_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleMuon", doFilter=True)
hlt_ElEl_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleEG", doFilter=True)
hlt_MuEl_Run2017CF = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.MuonEG", doFilter=True)

flags_MC2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="RunIISummer16", doFilter=True)
flags_Run2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="Run2016", doFilter=True)

flags_MC2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="RunIIFall17", doFilter=True)
flags_Run2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="Run2017", doFilter=True)
