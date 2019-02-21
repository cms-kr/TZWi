#!/bin/bash

if [ $# != 4 ]; then
    echo $#
    echo "Usage: ./run.sh MuEl MC.WW.txt 10 5 ## process WW sample assuming emu channel, split by 10 files and run 5th section"
    echo "Usage: ./run.sh ElEl MC.TT_powheg.txt 1 0"
    echo "Usage: ./run.sh MuMu RD.DoubleMuon_Run2016H.txt 1 0"
    exit 1
fi

eval `scram runtime -sh`

CHANNEL=$1
FILELIST=$2
MAXFILES=$3
JOBNUMBER=$4

DATATYPE1=`basename $FILELIST | sed -e 's;.txt;;g' | cut -d. -f1`
DATATYPE2=`basename $FILELIST | sed -e 's;.txt;;g' | cut -d. -f2 | cut -d_ -f2`
[ _$DATATYPE2 == _ ] && DATATYPE2=$DATATYPE1
[ _$DATATYPE1 == _RD -a $DATATYPE2 != Run2016H ] && DATATYPE2=Run2016BG
[ _$DATATYPE1 == _MC ] && DATATYPE2=MC

FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;/xrootd/;root://cms-xrdr.sdfarm.kr//xrd/;g')

ARGS=""
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLepton ttbar$CHANNEL"
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLeptonHLT ttbarHLT_${CHANNEL}_${DATATYPE2}"
ARGS="$ARGS -I TZWi.TopAnalysis.ttbarDoubleLeptonHLT flags_${DATATYPE1}"

OUTPATH=ntuple
CMD="nano_postproc.py --friend"
[ ! -d $OUTPATH ] && mkdir -p $OUTPATH
$CMD $ARGS $OUTPATH/reco $FILENAMES
if [ _$DATATYPE1 == "_MC" ]; then
    [ ! -d $OUTPATH/mc ] && mkdir -p $OUTPATH/mc
    ARGS=""
    #ARGS="" Add PUweights
    #ARGS="" Add other syst variations 
    $CMD $ARGS $OUTPATH/mc $FILENAMES

    if [ _$DATATYPE2 == "_TT" ]; then
        [ ! -d $OUTPATH/mctop ] && mkdir -p $OUTPATH/mctop
        ARGS="-I TZWi.TopAnalysis.partonTop partonTop"
        $CMD $ARGS $OUTPATH/mctop $FILENAMES
    fi
fi

