#!/bin/bash

eval `scram runtime -sh`

ERA=$1
CHANNEL=$2
FILELIST=$3
MAXFILES=$4
JOBNUMBER=$5

OUTPATH=ntuple
FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;/xrootd/;root://cms-xrdr.sdfarm.kr//xrd/;g')

[ ! -d $OUTPATH ] && mkdir -p $OUTPATH

ARGS=""
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLepton ttbar$CHANNEL"
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLeptonHLT ttbarHLT_${CHANNEL}_${ERA}"
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLeptonHLT flags_${ERA}"

nano_postproc.py --friend \
        $ARGS \
        $OUTPATH $FILENAMES
