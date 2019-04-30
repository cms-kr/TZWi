import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

hlt_MC2017_Mu = lambda : CombineHLT(fileName="fcnhSingleLepton/2017.yaml", hltSet="RunIIFall17.SingleMuon")
hlt_MC2017_El = lambda : CombineHLT(fileName="fcnhSingleLepton/2017.yaml", hltSet="RunIIFall17.SingleElectron")

hlt_Run2017_Mu = lambda : CombineHLT(fileName="fcnhSingleLepton/2017.yaml", hltSet="Run2017.SingleMuon"    , doFilter=True)
hlt_Run2017_El = lambda : CombineHLT(fileName="fcnhSingleLepton/2017.yaml", hltSet="Run2017.SingleElectron", doFilter=True)
