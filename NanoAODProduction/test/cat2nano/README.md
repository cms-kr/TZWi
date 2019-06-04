## Dump CAT-GenTops to NanoAOD format

1. Install NanoAOD and CATTools.
TZWi is just for a cfg file.

```
unset SCRAM_ARCH
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src/
cmsenv
git-cms-init

git cms-merge-topic cms-nanoAOD:master-102X
git checkout -b nanoAOD cms-nanoAOD/master-102X
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

git clone https://github.com/cms-kr/TZWi
git clone https://github.com/vallot/CATTools

scram b -j8
```

2. process over cattuples
```
cd TZWi/NanoAODProduction/test/cat2nano

BASEDIR=/xrootd/store/group/CAT/v8-0-8
SAMPLE=TT_TuneCUETP8M2T4_13TeV-powheg-pythia8
find $BASEDIR/$SAMPLE/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1 -name '*.root' | sed 's;/xrootd;;g' > $SAMPLE.txt

[ -d /xrootd_user/$USER/xrootd/NanoAOD/CATGenTop/20190604_1 ] || mkdir -p /xrootd_user/$USER/xrootd/NanoAOD/CATGenTop/20190604_1
create-batch --cfg genTopNano_cfg.py --fileList $SAMPLE.txt --maxFiles 1 --jobName $SAMPLE \
             --transferDest /store/user/$USER/NanoAOD/CATGenTop/20190604_1
```

