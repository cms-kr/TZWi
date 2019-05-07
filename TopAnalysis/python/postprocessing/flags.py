from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

flags_MC2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="RunIISummer16", doFilter=True)
flags_Run2016 = lambda : CombineHLT(outName="Flag", fileName="flags/2016.yaml", hltSet="Run2016", doFilter=True)

flags_MC2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="RunIIFall17", doFilter=True)
flags_Run2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="Run2017", doFilter=True)
