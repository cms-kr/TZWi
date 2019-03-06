from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.transferLogs    = False
config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = '2017_94XMiniAODv2_MC_TTbar_NANO.py'

config.section_("Data")
config.Data.publication  = False
#################################################################
# ALLOWS NON VALID DATASETS
config.Data.allowNonValidInputDataset = True

config.section_("Site")
# Where the output files will be transmitted to
#config.Site.storageSite = 'T2_KR_KNU'
#crab checkwrite --site=T3_KR_KISTI --lfn=/store/group/CAT/
config.Site.storageSite = 'T3_KR_KISTI'
#config.Site.storageSite = 'T3_KR_UOS'
#config.Site.storageSite = 'T3_US_FNALLPC'

#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

import os
#dataset = os.environ['DATASET']
dataset = '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
config.Data.inputDataset = dataset

reqName = "20190304"
config.Data.outLFNDirBase = '/store/user/yolee/nanottbb2017/%s' % reqName
label = dataset.split('/')[1]+'_'+dataset.split('/')[2]

config.Data.outputDatasetTag = label
#config.General.requestName = '%s_%s' % (reqName, label)
config.General.requestName = 'TT_only_MC'
#config.JobType.pyCfgParams = opts

#config.Data.lumiMask = "./Cert_294927-306126_13TeV_PromptReco_Collisions17_JSON.txt"

