#!/bin/bash

BASEDIR=/cms/ldap_home/jhgoh/work/CMS/NanoCAT/CMSSW_9_4_0/src/PhysicsTools/ChickenChicken/test/prod_ntuple
cd $BASEDIR
eval `scram runtime -sh`

FILELIST=$1
MAXFILES=$2
JOBNUMBER=$3

FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;/xrootd/;root://cms-xrdr.sdfarm.kr//xrd/;g')
OUTPATH=ntuple/`basename $FILELIST | sed -e 's;.txt;;g' -e 's;dataset_;;g'`
[ ! -d $OUTPATH ] && mkdir -p $OUTPATH

python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py --friend \
        -I PhysicsTools.ChickenChicken.topEvent.ttbarSingleLepton ttbarSingleLepton \
        $OUTPATH $FILENAMES
