import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

hlt_MC2016 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="RunIISummer16", doFilter=True)
hlt_MC2017 = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="RunIIFall17", doFilter=True)

for dataset in ['SingleMuon', 'SingleElectron',
                'DoubleMuon', 'DoubleEG', 'MuonEG']:
    if (dataset == ('SingleMuon' or 'SingleElectron')):
        for channel in ['MuEl', 'MuMu', 'ElEl']:
            for e in "BCDEFG":
                vars()["hlt_Run2016%s_%s_%s" % (e, dataset,channel)] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.%s.%s" % (dataset,channel), doFilter=True)
            vars()["hlt_Run2016H_%s_%s" % (dataset,channel)] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.%s.%s" % (dataset,channel), doFilter=True)                

    else:
        for e in "BCDEFG":
            vars()["hlt_Run2016%s_%s" % (e, dataset)] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016BG.%s" % dataset, doFilter=True)
        vars()["hlt_Run2016H_%s" % dataset] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2016.yaml", hltSet="Run2016H.%s" % dataset, doFilter=True)

    vars()["hlt_Run2017B_%s" % dataset] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017B.%s" % dataset, doFilter=True)
    for e in "CDEF":
        vars()["hlt_Run2017%s_%s" % (e, dataset)] = lambda : CombineHLT(fileName="ttbarDoubleLepton/2017.yaml", hltSet="Run2017CF.%s" % dataset, doFilter=True)

