#!/bin/bash

eval `scram runtime -sh`

FILELIST=$1
MAXFILES=$2
JOBNUMBER=$3

OUTPATH=`dirname $FILELIST`
OUTPATH=ntuple/`basename $OUTPATH`/`basename $FILELIST | sed -e 's;.txt;;g' -e 's;dataset_;;g'`
FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;/xrootd/;root://cms-xrdr.sdfarm.kr//xrd/;g')

[ ! -d $OUTPATH ] && mkdir -p $OUTPATH

echo python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py --friend \
        -I Kitten.TopAnalysis.ttbarDoubleLepton ttbarDoubleLepton \
        $OUTPATH $FILENAMES
