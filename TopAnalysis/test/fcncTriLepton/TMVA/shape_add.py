#! /bin/env python

import os, sys
import yaml
from glob import glob
from ROOT import *

processes_mapping = {
    'others' : ['SingleTop', 'WW', 'TTH']
}

if __name__ == '__main__':
    # Read input data
    rootDir = '%s/src/TZWi/TopAnalysis/test/fcncTriLepton/' % os.environ["CMSSW_BASE"]
    syst = ["origin", "jesUp", "jesDown", "jerUp", "jerDown"]
    #name for histogram
    syst_name = ["", "MuRDown", "MuFDown", "MuFUp", "MuRUp", "ElSFUp", "ElSFDown", "MuIDUp", "MuIDDown", "MuISOUp", "MuISODown", "PUUp", "PUDown", "BtagJESUp", "BtagJESDown", "BtagLFUp", "BtagLFDown", "BtagHFUp", "BtagHFDown", "BtagHFStats1Up", "BtagHFStats1Down", "BtagHFStats2Up", "BtagHFStats2Down", "BtagLFStats1Up", "BtagLFStats1Down", "BtagLFStats2Up", "BtagLFStats2Down", "BtagCQErr1Up", "BtagCQErr1Down", "BtagCQErr2Up", "BtagCQErr2Down"]

    channels = ["TTZct", "TTZut", "STZct", "STZut"]
    modes = ["ElElEl", "MuElEl", "ElMuMu", "MuMuMu"]

    procInfo = yaml.load(open(rootDir+"config/grouping.yaml").read())["processes"]
    crosssection = yaml.load(open(rootDir+"config/crosssection.yaml").read())["crosssection"]
    entries = yaml.load(open(rootDir+"config/crosssection.yaml").read())["Entries"]
    datasetInfo = {}
    for f in glob(rootDir+"config/datasets/MC*16*.yaml"):
        if 'dataset' not in datasetInfo: datasetInfo["dataset"] = {}
        datasetInfo["dataset"].update(yaml.load(open(f).read())["dataset"])
    if not os.path.exists( os.path.join(rootDir, 'TMVA', 'shape') ):
        os.makedirs(os.path.join(rootDir, 'TMVA', 'shape'))
    #Number of MVA score shape bins
    nbins = 10
    for ch in channels:
        outFileName = 'add_shape_%s' % ch
        outFile = TFile.Open( os.path.join(rootDir, 'TMVA', 'shape', outFileName + '.root'), 'RECREATE' )
        f_shape = TFile.Open( os.path.join(rootDir, 'TMVA', 'shape', 'shape_' + ch + '.root') )
        for mo in modes:
           hist_list = []
           no_overlap_hist_list = []
           merge_hist_sys_list = []
           merge_hist_jet_list = []
           nbins = 10
           for name in range(len(syst_name)):
               if name == 0: continue
               merge_hist_sys = TH1F(mo+"_others_" + syst_name[name], "mva shape %s" % syst_name[name], nbins, -1, 1)
               merge_hist_sys_list.append(merge_hist_sys)
           for jet_syst in syst:
               if jet_syst == "origin": merge_hist_jet = TH1F(mo + "_others", "mva shape origin", nbins, -1, 1)
               else: merge_hist_jet = TH1F(mo + "_others_" + jet_syst, "mva shape", nbins, -1, 1)
               merge_hist_jet_list.append(merge_hist_jet)

           for merge_name, origin_group in processes_mapping.items(): # merge_name: key, origin_group: value
               for category in origin_group:
                   for h_key in f_shape.GetListOfKeys(): #histogram name
                       if mo not in h_key.GetName(): continue
                       else:
                           if category in h_key.GetName():
                               for name in range(len(syst_name)):
                                   if name == 0: continue
                                   if h_key.GetName() == mo + "_" + category + "_" + syst_name[name]:
                                       for merge_hist_sys in merge_hist_sys_list:
                                           if mo + "_" + merge_name + "_" + syst_name[name] == merge_hist_sys.GetName():
                                               print h_key.GetName()
                                               hist = f_shape.Get(h_key.GetName())
                                               merge_hist_sys.Add(hist)
                               for jet_syst in syst:
                                   for merge_hist_jet in merge_hist_jet_list:
                                       if jet_syst == "origin" and h_key.GetName() == mo + "_" + category:
                                           print h_key.GetName()
                                           hist = f_shape.Get(h_key.GetName())
                                           if merge_hist_jet.GetName() == mo + "_" + merge_name: merge_hist_jet.Add(hist)
                                       elif jet_syst != "origin" and h_key.GetName() == mo + "_" + category + "_" + jet_syst:
                                           print h_key.GetName()
                                           hist = f_shape.Get(h_key.GetName())
                                           if merge_hist_jet.GetName() == mo + "_" + merge_name + "_" + jet_syst: merge_hist_jet.Add(hist)
                           else:
                               hist = f_shape.Get(h_key.GetName())
                               hist_list.append(hist)
           for h in hist_list:
               if h not in no_overlap_hist_list:
                   no_overlap_hist_list.append(h)
           outFile.cd()
           for h in no_overlap_hist_list:
               h.Write()
           for merge_h in merge_hist_sys_list:
               merge_h.Write()
           for merge_h in merge_hist_jet_list:
               merge_h.Write()
        outFile.Close()


