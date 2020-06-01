#!/usr/bin/env python
# @(#)root/tmva $Id$
# ------------------------------------------------------------------------------ #
# Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #
# Package      : TMVA                                                            #
# Python script: TMVAClassification.py                                           #
#                                                                                #
# This python script provides examples for the training and testing of all the   #
# TMVA classifiers through PyROOT.                                               #
#                                                                                #
# The Application works similarly, please see:                                   #
#    TMVA/macros/TMVAClassificationApplication.C                                 #
# For regression, see:                                                           #
#    TMVA/macros/TMVARegression.C                                                #
#    TMVA/macros/TMVARegressionpplication.C                                      #
# and translate to python as done here.                                          #
#                                                                                #
# As input data is used a toy-MC sample consisting of four Gaussian-distributed  #
# and linearly correlated input variables.                                       #
#                                                                                #
# The methods to be used can be switched on and off via the prompt command, for  #
# example:                                                                       #
#                                                                                #
#    python TMVAClassification.py --methods Fisher,Likelihood                    #
#                                                                                #
# The output file "TMVA.root" can be analysed with the use of dedicated          #
# macros (simply say: root -l <../macros/macro.C>), which can be conveniently    #
# invoked through a GUI that will appear at the end of the run of this macro.    #
#                                                                                #
# for help type "python TMVAClassification.py --help"                            #
# ------------------------------------------------------------------------------ #

# --------------------------------------------
# Standard python import
import sys    # exit
import time   # time accounting
import getopt # command line parser

# --------------------------------------------
import os
import yaml
from glob import glob

#options
print("Usage: python TMVAClassification.py mode -options")
print("Usage: python TMVAClassification.py --channel TTZct --mode ElElEl --method BDT,BDTG --outputfile fcnc_3El_TTZct_4bkg_BDT_G")
print("Usage: python TMVAClassification.py -C TTZct,TTZut -M ElElEl,MuElEl -m BDT,BDTG -o fcnc_3El_1Mu2El_TTsig_4bkg_BDT_G")
print("Usage: python TMVAClassification.py -C STZct,STZut -m BDT,BDTG -o fcnc_allCH_STsig_4bkg_BDT_G")
print("The weight directory name will be same to output name (result_+outputname)")

# Default settings for command line arguments
DEFAULT_OUTFNAME = "TMVA.root"
DEFAULT_INFNAME  = "tmva_class_example.root"
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
#DEFAULT_METHODS  = "Likelihood,LikelihoodD,MLPBNN,BDT,BDTG"
DEFAULT_METHODS = "BDT,BDTG,BDT850,BDT200,BDT100,BDT50"
DEFAULT_WEIGHTDIR = "dataset"
DEFAULT_MODE = ["ElElEl", "MuElEl", "MuMuMu", "ElMuMu"]
DEFAULT_CUT = ""
DEFAULT_CHANNEL = ["TTZct", "TTZut", "STZct", "STZut"]

# Print usage help
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -i | --inputfile  : name of input ROOT file (default: '%s')" % DEFAULT_INFNAME
    print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
          % (DEFAULT_TREESIG, DEFAULT_TREEBKG)
    print "  -M | --mode       : select mode [ElElEl, MuElEl, MuMuMu, ElMuMu] (default: all mode; '%s')" % DEFAULT_MODE
    print "  -C | --channel    : select signal MC (TTZct, TTZut, STZct, STZut) (default: all signal MC; '%s')" % DEFAULT_CHANNEL
    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:i:t:o:M:C:vh?"
        longopts   = ["methods=", "inputfile=", "inputtrees=", "outputfile=", "mode=", "channel=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )

    except getopt.GetoptError:
        # print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    #infname     = DEFAULT_INFNAME
    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    outfname    = DEFAULT_OUTFNAME
    methods     = DEFAULT_METHODS
    verbose     = False
    weightdir   = DEFAULT_WEIGHTDIR
    mode        = DEFAULT_MODE
    cut         = DEFAULT_CUT
    channel     = DEFAULT_CHANNEL
    
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-i", "--inputfile"):
            infname = a
        elif o in ("-o", "--outputfile"):
            outfname = a
            weightdir = 'result_' + a
        elif o in ("-t", "--inputtrees"):
            a.strip()
            trees = a.rsplit( ' ' )
            trees.sort()
            trees.reverse()
            if len(trees)-trees.count('') != 2:
                print "ERROR: need to give two trees (each one for signal and background)"
                print trees
                sys.exit(1)
            treeNameSig = trees[0]
            treeNameBkg = trees[1]
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-M", "--mode"):
            mode = a.replace(' ',',').split(',')
        elif o in ("-C", "--channel"):
            channel = a.replace(' ',',').split(',')

    # Print methods
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()

    # Import ROOT classes
    #from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
    from ROOT import *
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
    
    # Import TMVA classes from ROOT
    #from ROOT import TMVA
    TMVA.Tools.Instance()

    # Output file
    if not os.path.exists( 'output' ):
      os.makedirs('output')
    outdir = 'output/'
    outputFile = TFile( outdir+outfname+".root", 'RECREATE' )
    
    # Create instance of TMVA factory (see TMVA/macros/TMVAClassification.C for more factory options)
    # All TMVA output can be suppressed by removing the "!" (not) in 
    # front of the "Silent" argument in the option string
    factory = TMVA.Factory( "TMVAClassification", outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )

    # Set verbosity
    factory.SetVerbose( verbose )

    # If you wish to modify default settings 
    # (please check "src/Config.h" to see all available global options)
    #    gConfig().GetVariablePlotting()).fTimesRMS = 8.0
    #    gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory"

    dataloader = TMVA.DataLoader( "dataset" )
    TMVA.gConfig().GetIONames().fWeightFileDir = weightdir

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]

    #varListF = [
    #  "MVAinput_WLZL1_dPhi", "MVAinput_WLZL1_dR", "MVAinput_WLZL2_dPhi", "MVAinput_WLZL2_dR", "MVAinput_ZL1ZL2_dPhi", "MVAinput_ZL1ZL2_dR",
    #  "MVAinput_J1_DeepJetB", "MVAinput_J1_pt", "MVAinput_ZL1J1_dPhi", "MVAinput_ZL1J1_dR", "MVAinput_ZL2J1_dPhi", "MVAinput_ZL2J1_dR", "MVAinput_WLJ1_dPhi", "MVAinput_WLJ1_dR",
    #  "MVAinput_bJ_DeepJetB", "MVAinput_qJ_DeepJetB", "MVAinput_bJ_pt", "MVAinput_qJ_pt", "MVAinput_bJqJ_dPhi", "MVAinput_bJqJ_dR", 
    #  "MVAinput_WLbJ_dPhi", "MVAinput_WLbJ_dR", "MVAinput_WLqJ_dPhi", "MVAinput_WLqJ_dR", "MVAinput_ZL1bJ_dPhi", "MVAinput_ZL1bJ_dR", "MVAinput_ZL1qJ_dPhi", "MVAinput_ZL1qJ_dR",
    #  "MVAinput_ZL2bJ_dPhi", "MVAinput_ZL2bJ_dR", "MVAinput_ZL2qJ_dPhi", "MVAinput_ZL2qJ_dR",
    #  "Z_mass", "W_MT", 
    #]
    dataloader.AddVariable( "Z_mass","Z mass","", 'F' )
    dataloader.AddVariable( "W_MT", "Transeverse mass of W", "", "F" )
    dataloader.AddVariable( "MVAinput_bJ_DeepJetB", "DeepJetBtagger of FCNC jet", "", "F" )
    dataloader.AddVariable( "MVAinput_qJ_DeepJetB", "DeepJetBtagger of SM jet", "", "F" )
    dataloader.AddVariable( "MVAinput_WLqJ_dPhi", "dPhi of WL/FCNC jet", "", "F" )
    dataloader.AddVariable( "TriLepton_WleptonZdPhi", "dPhi of Z/WL", "", "F" )
    dataloader.AddVariable( "MVAinput_ZL1qJ_dR", "dR of ZL1/FCNC jet", "", "F" )
    dataloader.AddVariable( "MVAinput_ZL1bJ_dR", "dR of ZL1/SM jet", "", "F" )
    dataloader.AddVariable( "KinTopZq_mass", "FCNC Top mass", "", "F" )

    dataloader.AddVariable( "KinTopZq_eta", "eta of FCNC top", "", "F" )
    dataloader.AddVariable( "MVAinput_ZL1qJ_dPhi", "dPhi of lepton from Z and FCNC jet", "", "F" )
    dataloader.AddVariable( "MVAinput_WLqJ_dR", "dR of lepton from W and FCNC jet", "", "F" )
    dataloader.AddVariable( "MVAinput_bJqJ_dPhi", "dPhi of FCNC jet and SM jet","", "F" )
    dataloader.AddVariable( "TopTop_dPhi := abs(KinTopWb_phi-KinTopZq_phi)", "dPhi of SM top and FCNC top", "", "F" )
    dataloader.AddVariable( "MVAinput_WLZL1_dPhi", "dPhi of lepton from W and lepton from Z", "", "F" )

    # You can add so-called "Spectator variables", which are not used in the MVA training, 
    # but will appear in the final "TestTree" produced by TMVA. This TestTree will contain the 
    # input variables, the response values of all trained MVAs, and the spectator variables
    #factory.AddSpectator( "spec1:=var1*2",  "Spectator 1", "units", 'F' )
    #factory.AddSpectator( "spec2:=var1*3",  "Spectator 2", "units", 'F' )

    # Set individual event weights (the variables must exist in the original TTree)
    #    for signal    : factory.SetSignalWeightExpression    ("weight1*weight2");
    #    for background: factory.SetBackgroundWeightExpression("weight1*weight2");
    dataloader.SetWeightExpression("xsecNorm")

    dataloader.AddSpectator( "GoodLeptonCode" )
    dataloader.AddSpectator( "nGoodLepton" )
    dataloader.AddSpectator( "LeadingLepton_pt" )
    dataloader.AddSpectator( "Z_charge" )

    # Read input data
    #if gSystem.AccessPathName( infname ) != 0: gSystem.Exec( "wget http://root.cern.ch/files/" + infname )
    rootDir = '%s/src/TZWi/TopAnalysis/test/fcncTriLepton/' % os.environ["CMSSW_BASE"]
    ntupleDir = 'ntuple_2016'
    dName = rootDir + ntupleDir
    procInfo = yaml.load(open(rootDir+"config/grouping.yaml").read())["processes"]
    datasetInfo = {}
    #for f in glob(rootDir+"config/dataset/MC*16*.yaml"):
    #  for datasetGroup, dataset in yaml.load(open(f).read())['dataset'].iteritems():
    #    datasetInfo[datasetGroup] = dataset.keys()
    for f in glob(rootDir+"config/datasets/MC*16*.yaml"):
      if 'dataset' not in datasetInfo: datasetInfo["dataset"] = {}
      datasetInfo["dataset"].update(yaml.load(open(f).read())["dataset"])

    modes = mode

    fLists_sig = []
    fLists_bkg = []
    #Input list names are comes from 'title' at grouping.yaml
    #all signal title = ["STZct", "STZut", "TTZct", "TTZut"]
    #all background title = ["DYJets", "SingleTop", "ttJets", "ZZ", "WZ", "WW", "SingleTopV", "ttV", "ttH"]
    #High fraction bkgs in the Top pair Signal Region: ["DYJets", "ttJets", "ZZ", "WZ"]
    inputSigList = channel
    if DEFAULT_CHANNEL == channel:
      print("There are no particular signal region. No cut and all signals will be contained")
    inputBkgList = ["DYJets", "ttJets", "ZZ", "WZ"] #high fraction in the Top pair Signal Region: WZ > DYjet > ZZ > ttjet
    #inputBkgList = ["ZZ", "WZ"]
    #inputBkgList = ["DYJets", "ttJets"]
    #inputBkgList = ["DYJets", "SingleTop", "ttJets", "ZZ", "WZ", "WW", "SingleTopV", "ttV", "ttH"]

    for mo in modes:
      for proc in procInfo:
        if "Data" in procInfo[proc]['title']: continue
        for datasetGroup in procInfo[proc]['datasets']:
          #print(datasetGroup)
          #print(datasetInfo['dataset'][datasetGroup].keys())
          for datasetName in datasetInfo['dataset'][datasetGroup].keys():
            for inputSig in inputSigList:
              if ("FCNC" in datasetGroup) and (inputSig in procInfo[proc]['title']):
                fLists_sig.append(glob(dName+"/*/%s/%s" % (mo, datasetName[1:].replace('/','.'))))
            for inputBkg in inputBkgList:
              if ("FCNC" not in datasetGroup) and (inputBkg in procInfo[proc]['title']):
                fLists_bkg.append(glob(dName+"/*/%s/%s" % (mo, datasetName[1:].replace('/','.'))))
    print(fLists_sig)

    trees = []
    for fsig in fLists_sig:
      #print(fsig[0])
      signalWeight = 1.0
      file_list = os.listdir(fsig[0])
      for file_l in file_list:
        #print(file_l)
        f = TFile.Open(fsig[0]+"/"+file_l)
        t_sig = f.Get("Events")
        dataloader.AddSignalTree( t_sig, signalWeight )
        trees.append([f, t_sig])

    for fbkg in fLists_bkg:
      #print(fbkg[0])
      backgroundWeight = 1.0
      file_list = os.listdir(fbkg[0])
      for file_l in file_list:
        f = TFile.Open(fbkg[0]+"/"+file_l)
        t_bkg = f.Get("Events")
        if (t_bkg.GetEntries() == 0): break
        dataloader.AddBackgroundTree( t_bkg, backgroundWeight )
        trees.append([f, t_bkg])

    # Apply additional cuts on the signal and background sample.
 
    # TTSR
    if "TTZct" or "TTZut" in channel:
      mycutSig = TCut( "TMath::Abs(Z_mass-91.2)<7.5 && nGoodJet>=2 && nGoodJet<=3 && nBjet>=1 && GoodLeptonCode == 111 && nGoodLepton == 3 && LeadingLepton_pt >25 && Z_charge == 0 && W_MT <= 300" )
      mycutBkg = TCut( "TMath::Abs(Z_mass-91.2)<7.5 && nGoodJet>=2 && nGoodJet<=3 && nBjet>=1 && GoodLeptonCode == 111 && nGoodLepton == 3 && LeadingLepton_pt >25 && Z_charge == 0 && W_MT <= 300" )
    # STSR
    elif "STZct" or "STZut" in channel:
      mycutSig = TCut( "TMath::Abs(Z_mass-91.2)<7.5 && nGoodJet==1 && nBjet==1 && GoodLeptonCode == 111 && nGoodLepton == 3 && LeadingLepton_pt >25 && Z_charge == 0 && W_MT <= 300" )
      mycutBkg = TCut( "TMath::Abs(Z_mass-91.2)<7.5 && nGoodJet==1 && nBjet==1 && GoodLeptonCode == 111 && nGoodLepton == 3 && LeadingLepton_pt >25 && Z_charge == 0 && W_MT <= 300" )
    elif DEFAULT_CHANNEL == channel:
      mycutSig = TCut( cut )
      mycutBkg = TCut( cut )

    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    dataloader.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
    #
    # please lookup the various method configuration options in the corresponding cxx files, eg:
    # src/MethoCuts.cxx, etc, or here: http://tmva.sourceforge.net/optionRef.html
    # it is possible to preset ranges in the option string in which the cut optimisation should be done:
    # "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable

    # Cut optimisation

    # Likelihood ("naive Bayes estimator")
    if "Likelihood" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kLikelihood, "Likelihood",
                            "H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50" )

    # Decorrelated likelihood
    if "LikelihoodD" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kLikelihood, "LikelihoodD",
                            "!H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=50:VarTransform=Decorrelate" )

    if "MLPBNN" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kMLP, "MLPBNN", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:TrainingMethod=BFGS:UseRegulator" ) # BFGS training with bayesian regulators

    # Boosted Decision Trees
    if "BDTG" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDTG", "!H:!V:NTrees=400:MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2")

    if "BDT" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=400:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )

    if "BDT200" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDT200", "!H:!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )

    if "BDT100" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDT100", "!H:!V:NTrees=100:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )

    if "BDT850" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDT850", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )

    if "BDT50" in mlist:
        factory.BookMethod( dataloader, TMVA.Types.kBDT, "BDT50", "!H:!V:NTrees=50:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20" )



   # Multi-architecture DNN implementation.
    if ("DNN_CPU" or "DNN_GPU") in mlist:
      # General layout.
      layout = "Layout=TANH|128,TANH|128,TANH|128,LINEAR"
      dnnOptions = ["!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=N:WeightInitialization=XAVIERUNIFORM"]
      dnnOptions.append(layout)

      trainSteps = [
          ["LearningRate=1e-1","WeightDecay=1e-4","Momentum=0.9"],
          ["LearningRate=1e-2","WeightDecay=1e-4","Momentum=0.9"],
          ["LearningRate=1e-3","WeightDecay=1e-4","Momentum=0.0"],
      ]
      dropConfig = ["DropConfig=0.0+0.5+0.5+0.5", "DropConfig=0.0+0.0+0.0+0.0", "DropConfig=0.0+0.0+0.0+0.0"]
      trainStretagy0 = ["Repetitions=1","ConvergenceSteps=20","Regularization=L2","BatchSize=256","TestRepetitions=10","Multithreading=True"]
      dnnOptions.append("TrainingStrategy=%s" % ("|".join([",".join(trainStretagy0+steps+dropConfig) for steps in trainSteps])))

      # Cuda implementation.
      if "DNN_GPU" in mlist:
         dnnOptions.append("Architecture=GPU")
         factory.BookMethod(dataloader, TMVA.Types.kDNN, "DNN_GPU", ":".join(dnnOptions))

      # Multi-core CPU implementation.
      if "DNN_CPU" in mlist:
         dnnOptions.append("Architecture=CPU")
         factory.BookMethod(dataloader, TMVA.Types.kDNN, "DNN_CPU", ":".join(dnnOptions))



    # --------------------------------------------------------------------------------------------------
            
    # ---- Now you can tell the factory to train, test, and evaluate the MVAs. 

    # Train MVAs
    factory.TrainAllMethods()
    
    # Test MVAs
    factory.TestAllMethods()
    
    # Evaluate MVAs
    factory.EvaluateAllMethods()    
    
    # Save the output.
    outputFile.Close()
    
    print "=== wrote root file %s\n" % outfname
    print "=== TMVAClassification is done!\n"
    
    # open the GUI for the result macros    
    #TMVA.TMVAGui(outfname+".root")
    
    # keep the ROOT thread running
    #gApplication.Run() 

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
