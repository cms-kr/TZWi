#!/usr/bin/env python
import os, sys
from ROOT import *
from glob import glob
from array import array
import numpy as np
import yaml
from variables import input_TT_bdt, input_ST_bdt

# Import TMVA classes from ROOT
TMVA.Tools.Instance()

if len(sys.argv) < 2:
#-C TTZct -M MuMuMu -m BDTG200t1 -o TTZct_MuMuMu_except_WZ_ZZ_Tr7Te3
    print("Not enough arguments: channel, mode")
    print("Select one of the channel = TTZct, TTZut, STZct, STZut")
    print("Select one of the mode = ElElEl, MuElEl, MuMuMu, ElMuMu")
    print("Usage: python TMVAEvaluation_bdt.py TTZct ElElEl")
    sys.exit()
channel = sys.argv[1]
mode = sys.argv[2]

weight_bkg_case = 'WZ_ZZ'
# Weight outfile after classification in TT signal: channel_mode_WZ_ZZ_Tr7Te3/TMVAClassification_BDTG_TT.weights.xml

rootDir = '%s/src/TZWi/TopAnalysis/test/fcncTriLepton/' % os.environ["CMSSW_BASE"]
kisti_store = '/xrootd/store/user/heewon/'
ntupleDir = 'ntuple_2016'
weightDir = 'TMVA/dataset/result_%s_%s_%s_Tr7Te3' % (channel, mode, weight_bkg_case)
scoreDir = 'TMVA/scores/%s/%s_%s' % (channel, mode, weight_bkg_case)

#'title' in the groupting.yaml
#bkg_others = ["DYJets", "SingleTop", "ttJets", "WW", "SingleTopV", "ttV", "ttH"]

procInfo = yaml.load(open(rootDir+"config/grouping.yaml").read())["processes"]
datasetInfo = {}
for f in glob(rootDir+"config/datasets/*16*.yaml"):
      if 'dataset' not in datasetInfo: datasetInfo["dataset"] = {}
      datasetInfo["dataset"].update(yaml.load(open(f).read())["dataset"])

#for mc syst name
#syst = ["origin", "jesup", "jesdown", "jerup", "jerdown"]
#for btag weight
syst = ["origin"]
syst_btagshape = ["BtagWeight_btagSF_deepjet_shape_up_jes", "BtagWeight_btagSF_deepjet_shape_down_jes",
                 "BtagWeight_btagSF_deepjet_shape_up_lf", "BtagWeight_btagSF_deepjet_shape_down_lf",
                 "BtagWeight_btagSF_deepjet_shape_up_hf", "BtagWeight_btagSF_deepjet_shape_down_hf",
                 "BtagWeight_btagSF_deepjet_shape_up_hfstats1", "BtagWeight_btagSF_deepjet_shape_down_hfstats1",
                 "BtagWeight_btagSF_deepjet_shape_up_hfstats2", "BtagWeight_btagSF_deepjet_shape_down_hfstats2",
                 "BtagWeight_btagSF_deepjet_shape_up_lfstats1", "BtagWeight_btagSF_deepjet_shape_down_lfstats1",
                 "BtagWeight_btagSF_deepjet_shape_up_lfstats2", "BtagWeight_btagSF_deepjet_shape_down_lfstats2",
                 "BtagWeight_btagSF_deepjet_shape_up_cferr1", "BtagWeight_btagSF_deepjet_shape_down_cferr1",
                 "BtagWeight_btagSF_deepjet_shape_up_cferr2", "BtagWeight_btagSF_deepjet_shape_down_cferr2"]
syst_forWeight = ["Electron_SF", "Electron_SFerr", "MuonID_SF", "MuonID_SFerr", "MuonISO_SF", "MuonISO_SFerr", "Trigger_SF", "puWeight", "puWeightUp", "puWeightDown", "BtagWeight"]
#weight from origin: "LHEScaleWeight[4]*genWeight/abs(genWeight)*puWeight*BtagWeight*Trigger_SF*Electron_SF*MuonID_SF*MuonISO_SF
#ElSF up/down -> up/down: Electron_SF +- Electron_SFerr
#MuID up/down -> up/down: MuonID_SF +- MuonID_SFerr
#MuISO up/down -> up/down: MuonISO_SF +- MuonISO_SFerr
#syst_lepSF = ["ElSFUp", "ElSFDown", "MuIDUp", "MuIDDown", "MuISOUp", "MuISODown"]
#MuR up / down -> LHEScaleWeight[7] / [1]
#MuF up/down -> LHEScaleWeight[5] / [3]
#syst_theory = ["MuRUp", "MuRDown", "MuFUp", "MuFDown"]

#fLists_input = []
#We need to different variables for mva input by channel
input_features = []
if channel == "TTZct" or channel == "TTZut":
    input_features.extend(input_TT_bdt(channel))
elif channel == "STZct" or channel == "STZut":
    input_features.extend(input_ST_bdt(channel))
# Outfile will be processed by dataset from each syst
#for each_bkg in bkg_others:
#channel = sys.argv[1], mode = sys.argv[2]
for systjet in syst:
    if systjet == "jesup":
        ntupleDir = 'FCNC_2016_jesTotalUp'
        dName = kisti_store + ntupleDir
    elif systjet == "jesdown":
        ntupleDir = 'FCNC_2016_jesTotalDown'
        dName = kisti_store + ntupleDir
    elif systjet == "jerup":
        ntupleDir = 'FCNC_2016_jerUp'
        dName = kisti_store + ntupleDir
    elif systjet == "jerdown":
        ntupleDir = 'FCNC_2016_jerDown'
        dName = kisti_store + ntupleDir
    else:
        dName = rootDir + ntupleDir
    #if not os.path.exists( os.path.join(rootDir,scoreDir,systjet) ):
    #    os.makedirs( os.path.join(rootDir,scoreDir,systjet) )

    for proc in procInfo:
        #if each_bkg == procInfo[proc]['title']:
        #for each_mc in procInfo[proc]['title']:
        #if not "Data" in procInfo[proc]['title']:
        for datasetGroup in procInfo[proc]['datasets']:
            #print procInfo[proc]['modes'][0]
            if "Data" not in procInfo[proc]['title']:
                #datasetGroup = "MC2016.~~"
                #outputFile = TFile.Open( os.path.join(rootDir,scoreDir,systjet, 'score_TMVA_'+ datasetGroup[7:] + '.root'), 'RECREATE' )
                outputFile = TFile.Open( os.path.join(rootDir,scoreDir,systjet, 'score_TMVA_'+ datasetGroup[7:] + '.root'), 'UPDATE' )
            #elif ("Data" in procInfo[proc]['title']) and mode == procInfo[proc]['modes'][0] and ("NPL" not in procInfo[proc]['modes'][0]) and systjet=="origin":
            #    #datasetGroup = "Run2016.~~"
            #    print proc
            #    outputFile = TFile.Open( os.path.join(rootDir,scoreDir,systjet, 'score_TMVA_'+ datasetGroup[8:] + '.root'), 'RECREATE' )
            else: continue
            out_tree = TTree("EventsBtag", "EventsBtag")
            #out_tree = outputFile.Get("Events")
            fLists_input = []
            for datasetName in datasetInfo['dataset'][datasetGroup].keys():
                fLists_input.append(glob(dName+"/reco/%s/%s" % (mode, datasetName[1:].replace('/','.'))))

            #reader = TMVA.Reader("Color:!Silent") #coloured output & not suppression all output
            input_tree = TChain("Events")
            for fsig in fLists_input:
                print fsig[0]
                file_list = os.listdir(fsig[0])
                for file_l in file_list:
                    #f = TFile.Open(os.path.join(fsig[0],file_l))
                    #input_tree = f.Get("Events")
                    f = os.path.join(fsig[0],file_l)
                    input_tree.Add(f)

            branches = {}
            for branch in input_tree.GetListOfBranches():
                branchName = branch.GetName()
                if branchName in input_features:
                    branches[branchName] = array('f', [-999])
                    #reader.AddVariable(branchName, branches[branchName])
                    input_tree.SetBranchAddress(branchName, branches[branchName])
                #if branchName in ["LeadingLepton_pt", "Z_charge", "nGoodLepton", "GoodLeptonCode", "MVAinput_Status"]:
                #    branches[branchName] = array('f', [-999])
                #    reader.AddSpectator(branchName, branches[branchName])
                #if branchName in ["HLT", "nGoodJet", "nBjet"]:
                #    branches[branchName] = array('f', [-999])
                #    input_tree.SetBranchAddress(branchName, branches[branchName])
                #if branchName in syst_forWeight:
                #    branches[branchName] = array('f', [-999])
                #    input_tree.SetBranchAddress(branchName, branches[branchName])
                if branchName in syst_btagshape and systjet == "origin":
                    branches[branchName] = array('d', [-999])
                    input_tree.SetBranchAddress(branchName, branches[branchName])

            #if channel == "TTZct" or channel == "TTZut":
            #    reader.BookMVA('BDTG_TT', TString(os.path.join(rootDir,weightDir,'TMVAClassification_BDTG_TT.weights.xml')))
            #elif channel == "STZct" or channel == "STZut":
            #    reader.BookMVA('BDTG_ST', TString(os.path.join(rootDir,weightDir,'TMVAClassification_BDTG_ST.weights.xml')))
            totevent = input_tree.GetEntries()

            # for weight
            if "Data" not in procInfo[proc]['title']:
                if systjet == "origin":
                # for weight - btagshape
                    BtagWeight_jesup = np.zeros(1, dtype=np.float64)
                    BtagWeight_jesdown = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfup = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfdown = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfup = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfdown = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfstats1up = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfstats1down = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfstats1up = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfstats1down = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfstats2up = np.zeros(1, dtype=np.float64)
                    BtagWeight_lfstats2down = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfstats2up = np.zeros(1, dtype=np.float64)
                    BtagWeight_hfstats2down = np.zeros(1, dtype=np.float64)
                    BtagWeight_cferr1up = np.zeros(1, dtype=np.float64)
                    BtagWeight_cferr1down = np.zeros(1, dtype=np.float64)
                    BtagWeight_cferr2up = np.zeros(1, dtype=np.float64)
                    BtagWeight_cferr2down = np.zeros(1, dtype=np.float64)

            if "Data" not in procInfo[proc]['title']:
                if systjet == "origin":
                    out_tree.Branch('BtagWeight_jesup', BtagWeight_jesup, 'BtagWeight_jesup/D')
                    out_tree.Branch('BtagWeight_jesdown', BtagWeight_jesdown, 'BtagWeight_jesdown/D')
                    out_tree.Branch('BtagWeight_lfup', BtagWeight_lfup, 'BtagWeight_lfup/D')
                    out_tree.Branch('BtagWeight_lfdown', BtagWeight_lfdown, 'BtagWeight_lfdown/D')
                    out_tree.Branch('BtagWeight_hfup', BtagWeight_hfup, 'BtagWeight_hfup/D')
                    out_tree.Branch('BtagWeight_hfdown', BtagWeight_hfdown, 'BtagWeight_hfdown/D')
                    out_tree.Branch('BtagWeight_lfstats1up', BtagWeight_lfstats1up, 'BtagWeight_lfstats1up/D')
                    out_tree.Branch('BtagWeight_lfstats1down', BtagWeight_lfstats1down, 'BtagWeight_lfstats1down/D')
                    out_tree.Branch('BtagWeight_hfstats1up', BtagWeight_hfstats1up, 'BtagWeight_hfstats1up/D')
                    out_tree.Branch('BtagWeight_hfstats1down', BtagWeight_hfstats1down, 'BtagWeight_hfstats1down/D')
                    out_tree.Branch('BtagWeight_lfstats2up', BtagWeight_lfstats2up, 'BtagWeight_lfstats2up/D')
                    out_tree.Branch('BtagWeight_lfstats2down', BtagWeight_lfstats2down, 'BtagWeight_lfstats2down/D')
                    out_tree.Branch('BtagWeight_hfstats2up', BtagWeight_hfstats2up, 'BtagWeight_hfstats2up/D')
                    out_tree.Branch('BtagWeight_hfstats2down', BtagWeight_hfstats2down, 'BtagWeight_hfstats2down/D')
                    out_tree.Branch('BtagWeight_cferr1up', BtagWeight_cferr1up, 'BtagWeight_cferr1up/D')
                    out_tree.Branch('BtagWeight_cferr1down', BtagWeight_cferr1down, 'BtagWeight_cferr1down/D')
                    out_tree.Branch('BtagWeight_cferr2up', BtagWeight_cferr2up, 'BtagWeight_cferr2up/D')
                    out_tree.Branch('BtagWeight_cferr2down', BtagWeight_cferr2down, 'BtagWeight_cferr2down/D')

            print totevent
            for i in xrange(totevent):
                input_tree.GetEntry(i)
                if channel == "TTZct" or channel == "TTZut":
                    #TTSR
                    if not(input_tree.HLT == 1 and abs(input_tree.Z_mass-91.2) < 7.5 and input_tree.nGoodJet > 1 and input_tree.nGoodJet <= 3 and input_tree.nBjet >= 1 and abs(input_tree.GoodLeptonCode) == 111 and input_tree.nGoodLepton == 3 and input_tree.LeadingLepton_pt > 25 and input_tree.Z_charge == 0 and input_tree.W_MT <= 300): continue
                    if "Data" not in procInfo[proc]['title']:
                        if systjet == "origin":
                            BtagWeight_jesup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_jes
                            BtagWeight_jesdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_jes
                            BtagWeight_lfup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lf
                            BtagWeight_lfdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lf
                            BtagWeight_hfup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hf
                            BtagWeight_hfdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hf
                            BtagWeight_lfstats1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lfstats1
                            BtagWeight_lfstats1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lfstats1
                            BtagWeight_hfstats1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hfstats1
                            BtagWeight_hfstats1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hfstats1
                            BtagWeight_lfstats2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lfstats2
                            BtagWeight_lfstats2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lfstats2
                            BtagWeight_hfstats2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hfstats2
                            BtagWeight_hfstats2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hfstats2
                            BtagWeight_cferr1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_cferr1
                            BtagWeight_cferr1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_cferr1
                            BtagWeight_cferr2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_cferr2
                            BtagWeight_cferr2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_cferr2
                    out_tree.Fill()
                elif channel == "STZct" or channel == "STZut":
                    #STSR
                    if not(input_tree.HLT == 1 and abs(input_tree.Z_mass-91.2) < 7.5 and input_tree.nGoodJet == 1 and input_tree.nBjet == 1 and abs(input_tree.GoodLeptonCode) == 111 and input_tree.nGoodLepton == 3 and input_tree.LeadingLepton_pt > 25 and input_tree.Z_charge == 0 and input_tree.W_MT <= 300): continue
                    if "Data" not in procInfo[proc]['title']:
                        if systjet == "origin":
                            BtagWeight_jesup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_jes
                            BtagWeight_jesdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_jes
                            BtagWeight_lfup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lf
                            BtagWeight_lfdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lf
                            BtagWeight_hfup[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hf
                            BtagWeight_hfdown[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hf
                            BtagWeight_lfstats1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lfstats1
                            BtagWeight_lfstats1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lfstats1
                            BtagWeight_hfstats1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hfstats1
                            BtagWeight_hfstats1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hfstats1
                            BtagWeight_lfstats2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_lfstats2
                            BtagWeight_lfstats2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_lfstats2
                            BtagWeight_hfstats2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_hfstats2
                            BtagWeight_hfstats2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_hfstats2
                            BtagWeight_cferr1up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_cferr1
                            BtagWeight_cferr1down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_cferr1
                            BtagWeight_cferr2up[0] = input_tree.BtagWeight_btagSF_deepjet_shape_up_cferr2
                            BtagWeight_cferr2down[0] = input_tree.BtagWeight_btagSF_deepjet_shape_down_cferr2
                    out_tree.Fill()

            if "Data" not in procInfo[proc]['title']:
                if systjet == "origin":
                    BtagWeight_jesup[0] = BtagWeight_jesdown[0] = 0
                    BtagWeight_lfup[0] = BtagWeight_lfdown[0] = BtagWeight_hfup[0] = BtagWeight_hfdown[0] = 0
                    BtagWeight_lfstats1up[0] = BtagWeight_lfstats1down[0] = BtagWeight_hfstats1up[0] = BtagWeight_hfstats1down[0] = 0
                    BtagWeight_lfstats2up[0] = BtagWeight_lfstats2down[0] = BtagWeight_hfstats2up[0] = BtagWeight_hfstats2down[0] = 0
                    BtagWeight_cferr1up[0] = BtagWeight_cferr1down[0] = BtagWeight_cferr2up[0] = BtagWeight_cferr2down[0] = 0

            outputFile.Write()
            outputFile.Close()

