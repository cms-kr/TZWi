import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

### 2016 Logic
setFile = "ttbarDoubleLepton/2016.yaml"
hlt_MC2016 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer16", doFilter=True)
for channel in ['MuEl', 'MuMu', 'ElEl']:
    for dataset in ['DoubleMuon', 'DoubleEG', 'MuonEG']:
        for e in "BCDEFG":
            vars()["hlt_Run2016%s_%s" % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016BG.%s" % x, doFilter=True)
        vars()["hlt_Run2016H_%s" % dataset] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016H.%s" % x, doFilter=True)

    for dataset in ['SingleMuon', 'SingleElectron']:
        for e in "BCDEFG":
            vars()["hlt_Run2016%s_%s_%s" % (e, dataset,channel)] = lambda x=dataset, y=channel, f=setFile: CombineHLT(fileName=f, hltSet="Run2016BG.%s.%s" % (x,y), doFilter=True)
        vars()["hlt_Run2016H_%s_%s" % (dataset,channel)] = lambda x=dataset, y=channel, f=setFile: CombineHLT(fileName=f, hltSet="Run2016H.%s.%s" % (x,y), doFilter=True)

### 2017 Logic
setFile = "ttbarDoubleLepton/2017.yaml"
hlt_MC2017 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIIFall17", doFilter=True)
for dataset in ['DoubleMuon', 'DoubleEG', 'MuonEG']:
    vars()["hlt_Run2017B_%s" % dataset] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2017B.%s" % x, doFilter=True)
    for e in "CDEF":
        vars()["hlt_Run2017%s_%s" % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2017CF.%s" % x, doFilter=True)

