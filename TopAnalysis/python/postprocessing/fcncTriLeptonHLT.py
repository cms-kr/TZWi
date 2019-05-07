import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

hlt_MC2016 = lambda : CombineHLT(fileName="fcncTriLepton/2016.yaml", hltSet="RunIISummer16")

for dataset in ['SingleMuon', 'SingleElectron',
                'DoubleMuon', 'DoubleEG', 'MuonEG']:
    for e in "BCDE":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda : CombineHLT(fileName="fcncTriLepton/2016.yaml", hltSet="Run2016BE.%s" % dataset, doFilter=True)
    for e in "FG":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda : CombineHLT(fileName="fcncTriLepton/2016.yaml", hltSet="Run2016FG.%s" % dataset, doFilter=True)
    vars()['hlt_Run2016H_%s'  % dataset] = lambda : CombineHLT(fileName="fcncTriLepton/2016.yaml", hltSet="Run2016H.%s"  % dataset, doFilter=True)
