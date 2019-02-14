# TZWi
Yet another CMS NanoAOD tools focusing on specific analyses.

**See also**
- https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD

## Installation
```
cmsrel CMSSW_10_2_8
cd CMSSW_10_2_8/src
cmsenv
git-cms-init
git cms-merge-topic cms-nanoAOD:master-102X
git checkout -b nanoAOD cms-nanoAOD/master-102X
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/cms-kr/TZWi
scram b -j
```
