#!/bin/bash

if [ $# != 4 ]; then
    echo $#
    echo "Usage: $0 MuElEl MC2016.WW.txt 10 5 ## process WW sample assuming muee channel, split by 10 files and run 5th section"
    echo "Usage: $0 ElElEl MC2017.TT_powheg.txt 1 0 ## process TTbar sample assuming eee channel, one file per each section and run 0th one."
    echo "Usage: $0 MuMuMu Run2016B.DoubleMuon.txt 1 0"
    exit 1
fi

eval `scram runtime -sh`

CHANNEL=$1
FILELIST=$2
MAXFILES=$3
JOBNUMBER=$4

case $CHANNEL in
  MuElEl|ElMuEl)
    CHANNEL=ElElMu
    ;;
  ElMuMu|MuElMu)
    CHANNEL=MuMuEl
    ;;
esac

DATASET0=`basename $FILELIST | sed -e 's;.txt;;g'`
DATASET='/'`echo $DATASET0 | sed -e 's;\.;/;g'`
ERA=$(echo $DATASET0 | cut -d. -f2 | cut -d- -f1 | sed -e 's;NanoAOD;;g')

DATATYPE=$(basename $(dirname $FILELIST) | cut -d. -f1)
if [ ${DATATYPE::3} == "Run" ]; then
  HLTMODULE=${ERA::8}_$(echo $DATASET | cut -d/ -f2)
else
  HLTMODULE=$(echo $DATATYPE | cut -d_ -f1)
fi

FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;^/xrootd/;root://cms-xrdr.private.lo:2094//xrd/;g')

ARGS=""
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.flags flags_${DATATYPE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonHLT hlt_${HLTMODULE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLepton fcnc_${CHANNEL}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonCutFlow cutFlow_${CHANNEL}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.CopyBranch copyBranch"

OUTPATH=ntuple/reco/$CHANNEL/$DATASET0
CMD="nano_postproc.py --friend"
[ ! -d $OUTPATH ] && mkdir -p $OUTPATH
if [ ${DATATYPE::2} == "MC" ]; then
    ARGS="-I PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule countHistogramsModule $ARGS"
    ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.CopyBranch copyMCBranch"

    #ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer lepSF"
    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer puWeight"

    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF2016"
    ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.btagWeightProducer btagWeight"
fi
echo $CMD $ARGS $OUTPATH $FILENAMES
$CMD $ARGS $OUTPATH $FILENAMES
[ $? -eq 0 ] || echo $CMD $ARGS $OUTPATH $FILENAMES >> failed.txt

