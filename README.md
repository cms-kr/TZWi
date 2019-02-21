# TZWi
Yet another CMS NanoAOD tools focusing on specific analyses.
We'd like to cover:

  * ttbar dilepton analysis
    * inclusive cross section, differential cross section
    * ttbar+bbbar cross section ratio to ttbar+jets
  * ttbar rare decays
    * t->qZ, ttbar and single top

**See also**
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

## Installation
```
cmsrel CMSSW_10_2_11
cd CMSSW_10_2_11/src
cmsenv
git-cms-init
git cms-merge-topic cms-nanoAOD:master-102X
git checkout -b nanoAOD cms-nanoAOD/master-102X
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/cms-kr/TZWi
scram b -j
```

## Customized NanoAOD production
```
cd TZWi/NanoAODProduction/test
./generateConfig.sh ## This will produce 3 sets of 3 cfg files...
crab submit...
```

## Run postprocessors
```
cd TZWi/TopAnalysis/prod_ntuple
./run.sh .....
```
