#!/bin/bash

if [ $# != 3 ]; then
    echo $#
    echo "Usage: $0 2016All MC2016.WW.txt 1 ## apply JEC for 2016-all, process files in WW.txt, job section 1"
    exit 1
fi

eval `scram runtime -sh`

JECTYPE=$1
FILELIST=$2
JOBNUMBER=$3

FILENAME=$(cat $FILELIST | sed -n "$(($JOBNUMBER+1)) p" | sed 's;^/xrootd/;root://cms-xrdr.private.lo:2094//xrd/;g')
SUBDIR=`dirname $FILENAME | sed -e 's;^.*/store/;./store/;g'`

BRANCHSEL="$CMSSW_BASE/src/TZWi/NanoAODProduction/data/branchsel_JEC.txt"
CMD="nano_postproc.py --bo $BRANCHSEL"
ARGS="-I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertainties${JECTYPE}"

echo $CMD $ARGS $SUBDIR $FILENAME
$CMD $ARGS $SUBDIR $FILENAME
[ $? -eq 0 ] || echo $CMD $ARGS $SUBDIR $FILENAME >> failed.txt

