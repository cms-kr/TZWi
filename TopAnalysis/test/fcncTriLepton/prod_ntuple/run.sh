#!/bin/bash

if [ $# != 4 ]; then
    echo $#
    echo "Usage: ./run.sh MuElEl MC2016.WW.txt 10 5 ## process WW sample assuming muee channel, split by 10 files and run 5th section"
    echo "Usage: ./run.sh ElElEl MC2017.TT_powheg.txt 1 0 ## process TTbar sample assuming eee channel, one file per each section and run 0th one."
    echo "Usage: ./run.sh MuMuMu Run2016B.DoubleMuon.txt 1 0"
    exit 1
fi

eval `scram runtime -sh`

CHANNEL=$1
FILELIST=$2
MAXFILES=$3
JOBNUMBER=$4

[ $CHANNEL == 'MuElEl' ] && CHANNEL=ElElMu
[ $CHANNEL == 'ElMuMu' ] && CHANNEL=MuMuEl

DATATYPE0=`basename $FILELIST | sed -e 's;.txt;;g' | cut -d. -f1`
DATASET=`basename $FILELIST | sed -e 's;.txt;;g' | cut -d. -f2`
DATATYPE=$DATATYPE0
if [ ${DATATYPE::3} == "Run" ]; then
  DATATYPE=${DATATYPE::7} ## This gives Run2018A -> Run2018

  [ ${DATATYPE::8} == "Run2016BE" ] || [ ${DATATYPE::8} == "Run2016FG" ] || DATATYPE=Run2016H
fi

FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;/xrootd/;root://cms-xrdr.sdfarm.kr//xrd/;g')

ARGS=""
ARGS="$ARGS -I TZWi.TopAnalysis.fcncTriLepton fcnc_${CHANNEL}"
for MODE in E M MM EE ME; do
    ARGS="$ARGS -I TZWi.TopAnalysis.fcncTriLeptonHLT hlt_${MODE}_${DATATYPE}"
done
ARGS="$ARGS -I TZWi.TopAnalysis.fcncTriLeptonHLT flags_${DATATYPE}"
ARGS="$ARGS -I TZWi.TopAnalysis.fcncTriLeptonCutFlow cutFlow_${CHANNEL}"

OUTPATH=ntuple/reco
CMD="nano_postproc.py --friend"
[ ! -d $OUTPATH ] && mkdir -p $OUTPATH
#if [ ${DATATYPE::2} == "MC" ]; then
#    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer lepSF"
#    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puWeight"
#fi
echo $CMD $ARGS $OUTPATH $FILENAMES
$CMD $ARGS $OUTPATH $FILENAMES

