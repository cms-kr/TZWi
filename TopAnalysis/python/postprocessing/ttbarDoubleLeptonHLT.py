import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

hlt_MC2016_MuMu = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleMuon", doFilter=True)
hlt_MC2016_ElEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.DoubleEG", doFilter=True)
hlt_MC2016_MuEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16.MuonEG", doFilter=True)

hlt_MC2017_MuMu = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleMuon", doFilter=True)
hlt_MC2017_ElEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.DoubleEG", doFilter=True)
hlt_MC2017_MuEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17.MuonEG", doFilter=True)

for e in "BCDEFG":
    vars()["hlt_Run2016%s_MuMu" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleMuon", doFilter=True)
    vars()["hlt_Run2016%s_ElEl" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.DoubleEG", doFilter=True)
    vars()["hlt_Run2016%s_MuEl" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.MuonEG", doFilter=True)

hlt_Run2016H_MuMu = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleMuon", doFilter=True)
hlt_Run2016H_ElEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.DoubleEG", doFilter=True)
hlt_Run2016H_MuEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.MuonEG", doFilter=True)

hlt_Run2017B_MuMu = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleMuon", doFilter=True)
hlt_Run2017B_ElEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.DoubleEG", doFilter=True)
hlt_Run2017B_MuEl = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.MuonEG", doFilter=True)

for e in "CDEF":
    vars()["hlt_Run2017%s_MuMu" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleMuon", doFilter=True)
    vars()["hlt_Run2017%s_ElEl" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.DoubleEG", doFilter=True)
    vars()["hlt_Run2017%s_MuEl" % e] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.MuonEG", doFilter=True)

