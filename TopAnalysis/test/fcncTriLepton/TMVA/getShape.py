#!/usr/bin/env python
import yaml
import sys, os
from ROOT import *
from glob import glob
from array import array

if __name__ == '__main__':

    # Read input data
    rootDir = '%s/src/TZWi/TopAnalysis/test/fcncTriLepton/' % os.environ["CMSSW_BASE"]
    scoreDir = 'TMVA/scores'
    dName = rootDir + scoreDir
    syst = ["origin", "jesUp", "jesDown", "jerUp", "jerDown"]
    syst_btagshape = ["BtagWeight_jesup", "BtagWeight_jesdown",
                 "BtagWeight_lfup", "BtagWeight_lfdown", "BtagWeight_hfup", "BtagWeight_hfdown",
                 "BtagWeight_hfstats1up", "BtagWeight_hfstats1down", "BtagWeight_hfstats2up", "BtagWeight_hfstats2down",
                 "BtagWeight_lfstats1up", "BtagWeight_lfstats1down", "BtagWeight_lfstats2up", "BtagWeight_lfstats2down",
                 "BtagWeight_cferr1up", "BtagWeight_cferr1down", "BtagWeight_cferr2up", "BtagWeight_cferr2down"]
    syst_forWeight = ["LHEScaleWeight", "LHEScaleWeight_MuRUp", "LHEScaleWeight_MuRDown", "LHEScaleWeight_MuFUp", "LHEScaleWeight_MuFDown", "Electron_SF", "Electron_SFerr", "MuonID_SF", "MuonID_SFerr", "MuonISO_SF", "MuonISO_SFerr", "Trigger_SF", "puWeight", "puWeightUp", "puWeightDown", "BtagWeight"]
    #name for histogram
    syst_name = ["", "MuRDown", "MuFDown", "MuFUp", "MuRUp", "ElSFUp", "ElSFDown", "MuIDUp", "MuIDDown", "MuISOUp", "MuISODown", "PUUp", "PUDown", "BtagJESUp", "BtagJESDown", "BtagLFUp", "BtagLFDown", "BtagHFUp", "BtagHFDown", "BtagHFStats1Up", "BtagHFStats1Down", "BtagHFStats2Up", "BtagHFStats2Down", "BtagLFStats1Up", "BtagLFStats1Down", "BtagLFStats2Up", "BtagLFStats2Down", "BtagCQErr1Up", "BtagCQErr1Down", "BtagCQErr2Up", "BtagCQErr2Down"]
    #weight from origin: "LHEScaleWeight[4]*genWeight/abs(genWeight)*puWeight*BtagWeight*Trigger_SF*Electron_SF*MuonID_SF*MuonISO_SF
    #ElSF up/down -> up/down: Electron_SF +- Electron_SFerr
    #MuID up/down -> up/down: MuonID_SF +- MuonID_SFerr
    #MuISO up/down -> up/down: MuonISO_SF +- MuonISO_SFerr
    #syst_lepSF_name = ["ElSFUp", "ElSFDown", "MuIDUp", "MuIDDown", "MuISOUp", "MuISODown"]
    #MuR up / down -> LHEScaleWeight[7] / [1]
    #MuF up/down -> LHEScaleWeight[5] / [3]
    #syst_theory_name = ["MuRUp", "MuRDown", "MuFUp", "MuFDown"]

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
        outFileName = 'shape_%s' % ch
        outFile = TFile.Open( os.path.join(rootDir, 'TMVA', 'shape', outFileName + '.root'), 'RECREATE' )
        for mo in modes:
            hist_data = TH1F(mo+"_"+"data_obs", "mva shape data", nbins, -1, 1)
            for systjet in syst:
                for proc in procInfo:
                    #proc: DataElElEl, ... DataElMuMu, DataNPL..., DYJets, SingleTop, TTJets, STZct, ..., -> categories
                    hmc_mva_syst_list = []
                    if systjet == "origin":
                        if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                            if proc == ch:
                                hmc_jet = TH1F(mo+"_"+proc, "mva shape origin", nbins, -1, 1)
                            else: continue
                        else:
                            hmc_jet = TH1F(mo+"_"+proc, "mva shape origin", nbins, -1, 1)
                    else:
                        if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                            if proc == ch:
                                hmc_jet = TH1F(mo+"_"+proc+"_"+systjet, "mva shape", nbins, -1, 1)
                            else: continue
                        else:
                            hmc_jet = TH1F(mo+"_"+proc+"_"+systjet, "mva shape origin", nbins, -1, 1)
                    if systjet == "origin":
                        for name in range(len(syst_name)):
                            if name == 0: continue
                            if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                                if proc == ch:
                                    hmc_mva_syst = TH1F(mo+"_"+proc+"_"+syst_name[name], "mva shape %s" % syst_name[name], nbins, -1, 1)
                                    hmc_mva_syst_list.append(hmc_mva_syst)
                                else: continue
                            else:
                                hmc_mva_syst = TH1F(mo+"_"+proc+"_"+syst_name[name], "mva shape %s" % syst_name[name], nbins, -1, 1)
                                hmc_mva_syst_list.append(hmc_mva_syst)

                    for datasetGroup in procInfo[proc]['datasets']:
                        #datasetGroup: datasets in each category
                        #shape must be saved by each category.
                        weight_mc = 1
                        if "MC" in datasetGroup:
                            # Read score file
                            if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                                if proc == ch:
                                    f_score = TFile.Open(os.path.join(dName, ch, mo+'_WZ_ZZ', systjet, 'score_TMVA_'+datasetGroup[7:]+'.root' ))
                                else:
                                    print "This MC category is not signal"
                                    continue
                            else:
                                f_score = TFile.Open(os.path.join(dName, ch, mo+'_WZ_ZZ', systjet, 'score_TMVA_'+datasetGroup[7:]+'.root' ))
                            score_tree = f_score.Get("Events")
                            if systjet == "origin": score_tree_btag = f_score.Get("EventsBtag")

                            print systjet+"_"+datasetGroup[7:]

                            branches = {}
                            for branch in score_tree.GetListOfBranches():
                                branchName = branch.GetName()
                                if branchName in ["MLScore", "nEvent"]:
                                    branches[branchName] = array('f', [-999])
                                    score_tree.SetBranchAddress(branchName, branches[branchName])
                                if branchName in syst_forWeight:
                                    branches[branchName] = array('f', [-999])
                                    score_tree.SetBranchAddress(branchName, branches[branchName])
                            branches_b = {}
                            if systjet == "origin":
                                for branch in score_tree_btag.GetListOfBranches():
                                    branchName = branch.GetName()
                                    if (systjet == "origin") and (branchName in syst_btagshape):
                                        branches_b[branchName] = array('f', [-999])
                                        score_tree_btag.SetBranchAddress(branchName, branches_b[branchName])

                            xsec_num = 1.0
                            for xsec in crosssection:
                                for num in entries:
                                    if num == "TT":
                                        name = num + ".powheg"
                                    else:
                                        name = num
                                    if datasetGroup[7:] == name and num == xsec:
                                        xsec_num = (float(crosssection[xsec])/float(entries[num]))*35900
                            print xsec_num


                            totevent_score = score_tree.GetEntries()
                            for i in xrange(totevent_score):
                                score_tree.GetEntry(i)
                                if systjet == "origin":
                                    score_tree_btag.GetEntry(i)
                                    genWeight = score_tree.genWeight
                                    Trigger_SF = score_tree.Trigger_SF
                                    for name in range(len(syst_name)):
                                        if syst_name[name] == "MuRDown": LHEWeight = score_tree.LHEScaleWeight_MuRDown
                                        elif syst_name[name] == "MuFDown": LHEWeight = score_tree.LHEScaleWeight_MuFDown
                                        elif syst_name[name] == "MuFUp": LHEWeight = score_tree.LHEScaleWeight_MuFUp
                                        elif syst_name[name] == "MuRUp": LHEWeight = score_tree.LHEScaleWeight_MuRUp
                                        else: LHEWeight = score_tree.LHEScaleWeight

                                        if syst_name[name] == "ElSFUp": Ele_SF = score_tree.Electron_SF + score_tree.Electron_SFerr
                                        elif syst_name[name] == "ElSFDown": Ele_SF = score_tree.Electron_SF - score_tree.Electron_SFerr
                                        else: Ele_SF = score_tree.Electron_SF

                                        if syst_name[name] == "MuIDUp": MuID_SF = score_tree.MuonID_SF + score_tree.MuonID_SFerr
                                        elif syst_name[name] == "MuIDDown": MuID_SF = score_tree.MuonID_SF - score_tree.MuonID_SFerr
                                        else: MuID_SF = score_tree.MuonID_SF

                                        if syst_name[name] == "MuISOUp": MuISO_SF = score_tree.MuonISO_SF + score_tree.MuonISO_SFerr
                                        elif syst_name[name] == "MuISODown": MuISO_SF = score_tree.MuonISO_SF - score_tree.MuonISO_SFerr
                                        else: MuISO_SF = score_tree.MuonISO_SF

                                        if syst_name[name] == "PUUp": puWeight = score_tree.puWeightUp
                                        elif syst_name[name] == "PUDown": puWeight = score_tree.puWeightDown
                                        else: puWeight = score_tree.puWeight

                                        if "JESUp" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_jesup
                                        elif "JESDown" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_jesdown
                                        elif "LFUp" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfup
                                        elif "LFDown" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfdown
                                        elif "HFUp" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfup
                                        elif "HFDown" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfdown
                                        elif "HFStats1Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfstats1up
                                        elif "HFStats1Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfstats1down
                                        elif "HFStats2Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfstats2up
                                        elif "HFStats2Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_hfstats2down
                                        elif "LFStats1Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfstats1up
                                        elif "LFStats1Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfstats1down
                                        elif "LFStats2Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfstats2up
                                        elif "LFStats2Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_lfstats2down
                                        elif "CQErr1Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_cferr1up
                                        elif "CQErr1Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_cferr1down
                                        elif "CQErr2Up" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_cferr2up
                                        elif "CQErr2Down" in syst_name[name]: btagWeight = score_tree_btag.BtagWeight_cferr2down
                                        else: btagWeight = score_tree.BtagWeight

                                        weight_mc *= LHEWeight*genWeight/abs(genWeight)*puWeight*btagWeight*Trigger_SF*Ele_SF*MuID_SF*MuISO_SF*xsec_num
                                        if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                                            if proc in hmc_jet.GetName(): #for signal MC
                                                if syst_name[name] == "": hmc_jet.Fill(score_tree.MLScore, weight_mc)
                                                elif syst_name[name] != "" and name != 0:
                                                    for hist in hmc_mva_syst_list:
                                                        if syst_name[name] in hist.GetName():
                                                            hist.Fill(score_tree.MLScore, weight_mc)
                                                        else: continue
                                                else: continue
                                            else: continue
                                        else:
                                            if syst_name[name] == "": hmc_jet.Fill(score_tree.MLScore, weight_mc)
                                            elif syst_name[name] != "" and name != 0:
                                                for hist in hmc_mva_syst_list:
                                                    if syst_name[name] in hist.GetName():
                                                        hist.Fill(score_tree.MLScore, weight_mc)
                                                    else: continue
                                            else: continue
                                        weight_mc = 1
                                elif systjet != "origin":
                                    genWeight = score_tree.genWeight
                                    Trigger_SF = score_tree.Trigger_SF
                                    LHEWeight = score_tree.LHEScaleWeight
                                    Ele_SF = score_tree.Electron_SF
                                    MuID_SF = score_tree.MuonID_SF
                                    MuISO_SF = score_tree.MuonISO_SF
                                    puWeight = score_tree.puWeight
                                    btagWeight = score_tree.BtagWeight
                                    weight_mc *= LHEWeight*genWeight/abs(genWeight)*puWeight*btagWeight*Trigger_SF*Ele_SF*MuID_SF*MuISO_SF*xsec_num
                                    if proc == "TTZct" or proc == "TTZut" or proc == "STZct" or proc == "STZut":
                                        if proc in hmc_jet.GetName(): hmc_jet.Fill(score_tree.MLScore, weight_mc)
                                    else: hmc_jet.Fill(score_tree.MLScore, weight_mc)
                                    weight_mc = 1
                                else:
                                    print "!!Fail!!"
                            f_score.Close()

                        elif "Run" in datasetGroup:
                            if ("Data" in procInfo[proc]['title']) and mo == procInfo[proc]['modes'][0] and ("NPL" not in procInfo[proc]['modes'][0]) and systjet=="origin":
                                f_score = TFile.Open(os.path.join(dName, ch, mo+'_WZ_ZZ', systjet, 'score_TMVA_'+datasetGroup[8:]+'.root'))
                                score_tree = f_score.Get("Events")
                                totevent_score = score_tree.GetEntries()
                                print datasetGroup[8:]
                                branches = {}
                                for branch in score_tree.GetListOfBranches():
                                    branchName = branch.GetName()
                                    if branchName in ["MLScore", "nEvent"]:
                                        branches[branchName] = array('f', [-999])
                                        score_tree.SetBranchAddress(branchName, branches[branchName])

                                for i in xrange(totevent_score):
                                    score_tree.GetEntry(i)
                                    hist_data.Fill(score_tree.MLScore)
                                f_score.Close()
                    outFile.cd()
                    if not "Data" in proc:
                        hmc_jet.Write()
                        for hist in hmc_mva_syst_list:
                            hist.Write()
                    if "Data" in proc and mo == procInfo[proc]['modes'][0] and ("NPL" not in procInfo[proc]['modes'][0]) and systjet=="origin":
                        hist_data.Write()
        outFile.Close()
