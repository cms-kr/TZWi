import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

setFile = "fcncTriLepton/2016.yaml"
hlt_MC2016 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer16")
for dataset in ['SingleMuon', 'SingleElectron',
                'DoubleMuon', 'DoubleEG', 'MuonEG']:
    for e in "BCDE":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016BE.%s" % x, doFilter=True)
    for e in "FG":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016FG.%s" % x, doFilter=True)
    vars()['hlt_Run2016H_%s'  % dataset] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016H.%s"  % x, doFilter=True)
