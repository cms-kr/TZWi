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
syst = ["origin", "jesUp", "jesDown", "jerUp", "jerDown"]
syst_forWeight = ["genWeight", "Electron_SF", "Electron_SFerr", "MuonID_SF", "MuonID_SFerr", "MuonISO_SF", "MuonISO_SFerr", "Trigger_SF", "puWeight", "puWeightUp", "puWeightDown", "BtagWeight"]
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
    if systjet == "jesUp":
        ntupleDir = 'FCNC_2016_jesTotalUp'
        dName = kisti_store + ntupleDir
    elif systjet == "jesDown":
        ntupleDir = 'FCNC_2016_jesTotalDown'
        dName = kisti_store + ntupleDir
    elif systjet == "jerUp":
        ntupleDir = 'FCNC_2016_jerUp'
        dName = kisti_store + ntupleDir
    elif systjet == "jerDown":
        ntupleDir = 'FCNC_2016_jerDown'
        dName = kisti_store + ntupleDir
    else:
        dName = rootDir + ntupleDir
    if not os.path.exists( os.path.join(rootDir,scoreDir,systjet) ):
        os.makedirs( os.path.join(rootDir,scoreDir,systjet) )

    for proc in procInfo:
        #if each_bkg == procInfo[proc]['title']:
        #for each_mc in procInfo[proc]['title']:
        #if not "Data" in procInfo[proc]['title']:
        for datasetGroup in procInfo[proc]['datasets']:
            #print procInfo[proc]['modes'][0]
            if "Data" not in procInfo[proc]['title']:
                #datasetGroup = "MC2016.~~"
                outputFile = TFile.Open( os.path.join(rootDir,scoreDir,systjet, 'score_TMVA_'+ datasetGroup[7:] + '.root'), 'RECREATE' )
            elif ("Data" in procInfo[proc]['title']) and mode == procInfo[proc]['modes'][0] and ("NPL" not in procInfo[proc]['modes'][0]) and systjet=="origin":
                #datasetGroup = "Run2016.~~"
                print proc
                outputFile = TFile.Open( os.path.join(rootDir,scoreDir,systjet, 'score_TMVA_'+ datasetGroup[8:] + '.root'), 'RECREATE' )
            else: continue
            out_tree = TTree("Events", "Events")
            fLists_input = []
            for datasetName in datasetInfo['dataset'][datasetGroup].keys():
                fLists_input.append(glob(dName+"/reco/%s/%s" % (mode, datasetName[1:].replace('/','.'))))

            reader = TMVA.Reader("Color:!Silent") #coloured output & not suppression all output
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
                    reader.AddVariable(branchName, branches[branchName])
                    input_tree.SetBranchAddress(branchName, branches[branchName])
                if branchName in ["LeadingLepton_pt", "Z_charge", "nGoodLepton", "GoodLeptonCode", "MVAinput_Status"]:
                    branches[branchName] = array('f', [-999])
                    reader.AddSpectator(branchName, branches[branchName])
                if branchName in ["HLT", "nGoodJet", "nBjet"]:
                    branches[branchName] = array('f', [-999])
                    input_tree.SetBranchAddress(branchName, branches[branchName])
                if branchName in syst_forWeight:
                    branches[branchName] = array('f', [-999])
                    input_tree.SetBranchAddress(branchName, branches[branchName])

            if channel == "TTZct" or channel == "TTZut":
                reader.BookMVA('BDTG_TT', TString(os.path.join(rootDir,weightDir,'TMVAClassification_BDTG_TT.weights.xml')))
            elif channel == "STZct" or channel == "STZut":
                reader.BookMVA('BDTG_ST', TString(os.path.join(rootDir,weightDir,'TMVAClassification_BDTG_ST.weights.xml')))
            totevent = input_tree.GetEntries()

            score = np.zeros(1, dtype=np.float32)
            nEvent = np.zeros(1, dtype=int)
            nGoodLepton = np.zeros(1, dtype=int)
            LeadingLepton_pt = np.zeros(1, dtype=np.float32)
            Z_charge = np.zeros(1, dtype=int)
            MVAinput_Status = np.zeros(1, dtype=int)
            # for weight
            if "Data" not in procInfo[proc]['title']:
                genWeight = np.zeros(1, dtype=np.float32)
                LHEScaleWeight = np.zeros(1, dtype=np.float32)
                LHEScaleWeight_MuRUp = np.zeros(1, dtype=np.float32)
                LHEScaleWeight_MuRDown = np.zeros(1, dtype=np.float32)
                LHEScaleWeight_MuFUp = np.zeros(1, dtype=np.float32)
                LHEScaleWeight_MuFDown = np.zeros(1, dtype=np.float32)
                Electron_SF = np.zeros(1, dtype=np.float32)
                Electron_SFerr = np.zeros(1, dtype=np.float32)
                MuonID_SF = np.zeros(1, dtype=np.float32)
                MuonID_SFerr = np.zeros(1, dtype=np.float32)
                MuonISO_SF = np.zeros(1, dtype=np.float32)
                MuonISO_SFerr = np.zeros(1, dtype=np.float32)
                Trigger_SF = np.zeros(1, dtype=np.float32)
                puWeight = np.zeros(1, dtype=np.float32)
                puWeightUp = np.zeros(1, dtype=np.float32)
                puWeightDown = np.zeros(1, dtype=np.float32)
                BtagWeight = np.zeros(1, dtype=np.float64)

            if "Data" not in procInfo[proc]['title']:
                out_tree.Branch('genWeight', genWeight, 'genWeight/F')
                out_tree.Branch('LHEScaleWeight', LHEScaleWeight, 'LHEScaleWeight/F')
                out_tree.Branch('LHEScaleWeight_MuRUp', LHEScaleWeight_MuRUp, 'LHEScaleWeight_MuRUp/F')
                out_tree.Branch('LHEScaleWeight_MuRDown', LHEScaleWeight_MuRDown, 'LHEScaleWeight_MuRDown/F')
                out_tree.Branch('LHEScaleWeight_MuFUp', LHEScaleWeight_MuFUp, 'LHEScaleWeight_MuFUp/F')
                out_tree.Branch('LHEScaleWeight_MuFDown', LHEScaleWeight_MuFDown, 'LHEScaleWeight_MuFDown/F')
                out_tree.Branch('Electron_SF', Electron_SF, 'Electron_SF/F')
                out_tree.Branch('Electron_SFerr', Electron_SFerr, 'Electron_SFerr/F')
                out_tree.Branch('MuonID_SF', MuonID_SF, 'MuonID_SF/F')
                out_tree.Branch('MuonID_SFerr', MuonID_SFerr, 'MuonID_SFerr/F')
                out_tree.Branch('MuonISO_SF', MuonISO_SF, 'MuonISO_SF/F')
                out_tree.Branch('MuonISO_SFerr', MuonISO_SFerr, 'MuonISO_SFerr/F')
                out_tree.Branch('Trigger_SF', Trigger_SF, 'Trigger_SF/F')
                out_tree.Branch('puWeight', puWeight, 'puWeight/F')
                out_tree.Branch('puWeightUp', puWeightUp, 'puWeightUp/F')
                out_tree.Branch('puWeightDown', puWeightDown, 'puWeightDown/F')
                out_tree.Branch('BtagWeight', BtagWeight, 'BtagWeight/D')

            out_tree.Branch('MLScore', score, 'MLScore/F')
            out_tree.Branch('LeadingLepton_pt', LeadingLepton_pt, 'LeadingLepton_pt/F')
            out_tree.Branch('Z_charge', Z_charge, 'Z_charge/I')
            out_tree.Branch('nEvent', nEvent, 'nEvent/I')
            out_tree.Branch('nGoodLepton', nGoodLepton, 'nGoodLepton/I')
            out_tree.Branch('MVAinput_Status', MVAinput_Status, 'MVAinput_Status/i')

            print totevent
            for i in xrange(totevent):
                input_tree.GetEntry(i)
                if channel == "TTZct" or channel == "TTZut":
                    #TTSR
                    if not(input_tree.HLT == 1 and abs(input_tree.Z_mass-91.2) < 7.5 and input_tree.nGoodJet > 1 and input_tree.nGoodJet <= 3 and input_tree.nBjet >= 1 and abs(input_tree.GoodLeptonCode) == 111 and input_tree.nGoodLepton == 3 and input_tree.LeadingLepton_pt > 25 and input_tree.Z_charge == 0 and input_tree.W_MT <= 300): continue
                    score[0] = reader.EvaluateMVA('BDTG_TT')
                    nEvent[0] = input_tree.event
                    nGoodLepton[0] = input_tree.nGoodLepton
                    LeadingLepton_pt[0] = input_tree.LeadingLepton_pt
                    Z_charge[0] = input_tree.Z_charge
                    MVAinput_Status[0] = input_tree.MVAinput_Status
                    if "Data" not in procInfo[proc]['title']:
                    #MuR up / down -> LHEScaleWeight[7] / [1]
                    #MuF up/down -> LHEScaleWeight[5] / [3]
                        if not input_tree.LHEScaleWeight:
                            LHEScaleWeight[0] = LHEScaleWeight_MuRUp[0] = LHEScaleWeight_MuRDown[0] = LHEScaleWeight_MuFUp[0] = LHEScaleWeight_MuFDown[0] = 0
                            print "No LHEScaleWeight! Checking the genWeight and original LHEWeight from this input"
                        else:
                            LHEScaleWeight[0] = input_tree.LHEScaleWeight[4]
                            LHEScaleWeight_MuRUp[0] = input_tree.LHEScaleWeight[7]
                            LHEScaleWeight_MuRDown[0] = input_tree.LHEScaleWeight[1]
                            LHEScaleWeight_MuFUp[0] = input_tree.LHEScaleWeight[5]
                            LHEScaleWeight_MuFDown[0] = input_tree.LHEScaleWeight[3]
                        genWeight[0] = input_tree.genWeight
                        Electron_SF[0] = input_tree.Electron_SF
                        Electron_SFerr[0] = input_tree.Electron_SFerr
                        MuonID_SF[0] = input_tree.MuonID_SF
                        MuonID_SFerr[0] = input_tree.MuonID_SFerr
                        MuonISO_SF[0] = input_tree.MuonID_SF
                        MuonISO_SFerr[0] = input_tree.MuonID_SFerr
                        Trigger_SF[0] = input_tree.Trigger_SF
                        puWeight[0] = input_tree.puWeight
                        puWeightUp[0] = input_tree.puWeightUp
                        puWeightDown[0] = input_tree.puWeightDown
                        BtagWeight[0] = input_tree.BtagWeight
                    out_tree.Fill()
                elif channel == "STZct" or channel == "STZut":
                    #STSR
                    if not(input_tree.HLT == 1 and abs(input_tree.Z_mass-91.2) < 7.5 and input_tree.nGoodJet == 1 and input_tree.nBjet == 1 and abs(input_tree.GoodLeptonCode) == 111 and input_tree.nGoodLepton == 3 and input_tree.LeadingLepton_pt > 25 and input_tree.Z_charge == 0 and input_tree.W_MT <= 300): continue
                    score[0] = reader.EvaluateMVA('BDTG_ST')
                    nEvent[0] = input_tree.event
                    nGoodLepton[0] = input_tree.nGoodLepton
                    LeadingLepton_pt[0] = input_tree.LeadingLepton_pt
                    Z_charge[0] = input_tree.Z_charge
                    MVAinput_Status[0] = input_tree.MVAinput_Status
                    if "Data" not in procInfo[proc]['title']:
                        if not input_tree.LHEScaleWeight:
                            LHEScaleWeight[0] = LHEScaleWeight_MuRUp[0] = LHEScaleWeight_MuRDown[0] = LHEScaleWeight_MuFUp[0] = LHEScaleWeight_MuFDown[0] = 0
                            print "No LHEScaleWeight! Checking the genWeight and original LHEWeight from this input"
                        else:
                            LHEScaleWeight[0] = input_tree.LHEScaleWeight[4]
                            LHEScaleWeight_MuRUp[0] = input_tree.LHEScaleWeight[7]
                            LHEScaleWeight_MuRDown[0] = input_tree.LHEScaleWeight[1]
                            LHEScaleWeight_MuFUp[0] = input_tree.LHEScaleWeight[5]
                            LHEScaleWeight_MuFDown[0] = input_tree.LHEScaleWeight[3]
                        genWeight[0] = input_tree.genWeight
                        Electron_SF[0] = input_tree.Electron_SF
                        Electron_SFerr[0] = input_tree.Electron_SFerr
                        MuonID_SF[0] = input_tree.MuonID_SF
                        MuonID_SFerr[0] = input_tree.MuonID_SFerr
                        MuonISO_SF[0] = input_tree.MuonID_SF
                        MuonISO_SFerr[0] = input_tree.MuonID_SFerr
                        Trigger_SF[0] = input_tree.Trigger_SF
                        puWeight[0] = input_tree.puWeight
                        puWeightUp[0] = input_tree.puWeightUp
                        puWeightDown[0] = input_tree.puWeightDown
                        BtagWeight[0] = input_tree.BtagWeight
                    out_tree.Fill()

            score[0] = -1
            nEvent[0] = 0
            nGoodLepton[0] = 0
            LeadingLepton_pt[0] = 0
            Z_charge[0] = 0
            MVAinput_Status[0] = 0
            if "Data" not in procInfo[proc]['title']:
                LHEScaleWeight[0] = 0
                LHEScaleWeight_MuRUp[0] = 0
                LHEScaleWeight_MuRDown[0] = 0
                LHEScaleWeight_MuFUp[0] = 0
                LHEScaleWeight_MuFDown[0] = 0
                genWeight[0] = 0
                Electron_SF[0] = Electron_SFerr[0] = 0
                MuonID_SF[0] = MuonID_SFerr[0] = MuonISO_SF[0] = MuonISO_SFerr[0] = 0
                Trigger_SF[0] = 0
                puWeight[0] = puWeightUp[0] = puWeightDown[0] = 0
                BtagWeight[0] = 0

            outputFile.Write()
            outputFile.Close()

