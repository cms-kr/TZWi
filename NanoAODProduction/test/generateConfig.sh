#!/bin/bash
## Check GT from the official twiki
## https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions

OPTS_COMMON="-s NANO --no_exec"
OPTS_MC="--mc --eventcontent NANOAODSIM --datatier NANOAODSIM"
OPTS_RC="--data --eventcontent NANOAOD --datatier NANOAOD"
CUSTOMBASE="TZWi/NanoAODProduction/customise_cff"

CUSTOMISE_TOP="${CUSTOMBASE}.customise_dropNanoAODTables,${CUSTOMBASE}.customise_particleTop"
CUSTOMISE_TOP="${CUSTOMISE_TOP},${CUSTOMBASE}.customise_partonTop"

## 2016
ERA="Run2_2016,run2_miniAOD_80XLegacy"
#ERA="Run2_2016,run2_nanoAOD_94X2016"
GT_MC="80X_mcRun2_asymptotic_2016_TrancheIV_v8" ## For 02Feb2017
GT_RD="80X_dataRun2_2016SeptRepro_v7" ## reMiniAod 02Feb2017 campaign

cmsDriver.py 2016_80XLegacy_RD $OPTS_COMMON $OPTS_RD --conditions $GT_RD
cmsDriver.py 2016_80XLegacy_MC $OPTS_COMMON $OPTS_MC --conditions $GT_MC
cmsDriver.py 2016_80XLegacy_MC_TTbar $OPTS_COMMON $OPTS_MC --conditions $GT_MC --customise $CUSTOMISE_TOP

## 2017
ERA="Run2_2017,run2_nanoAOD_94XMiniAODv2"
GT_MC="94X_mc2017_realistic_v14" ## 
GT_RD="94X_dataRun2_v6" ## 

cmsDriver.py 2017_94XMiniAODv2_RD $OPTS_COMMON $OPTS_RD --conditions $GT_RD
cmsDriver.py 2017_94XMiniAODv2_MC $OPTS_COMMON $OPTS_MC --conditions $GT_MC
cmsDriver.py 2017_94XMiniAODv2_MC_TTbar $OPTS_COMMON $OPTS_MC --conditions $GT_MC --customise $CUSTOMISE_TOP

## 2018
ERA="Run2_2018"
GT_MC="100X_upgrade2018_realistic_v10" ## RunIISpring18MiniAOD campaign
GT_RD="101X_dataRun2_Prompt_v11" ## PromptReco 2018

cmsDriver.py 2018_v0_RD $OPTS_COMMON $OPTS_RD --conditions $GT_RD
cmsDriver.py 2018_v0_MC $OPTS_COMMON $OPTS_MC --conditions $GT_MC
cmsDriver.py 2018_v0_MC_TTbar $OPTS_COMMON $OPTS_MC --conditions $GT_MC --customise $CUSTOMISE_TOP

