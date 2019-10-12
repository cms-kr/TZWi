import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

###2016
setFile = "fcncTriLepton/2016.yaml"
hlt_MC2016 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer16")
for dataset in ['DoubleMuon', 'DoubleEG']:
    for e in "BCDEFG":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016BG.%s" % x, doFilter=True)
    vars()['hlt_Run2016H_%s'  % dataset] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016H.%s"  % x, doFilter=True)

###2017
setFile = "fcncTriLepton/2017.yaml"
hlt_MC2017 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIIFall17")
for dataset in ['SingleMuon', 'SingleElectron',
                'DoubleMuon', 'DoubleEG', 'MuonEG']:
    vars()['hlt_Run2017B_%s'  % dataset] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2017B.%s"  % x, doFilter=True)
    for e in "CDEF":
        vars()['hlt_Run2017%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2017CF.%s" % x, doFilter=True)
