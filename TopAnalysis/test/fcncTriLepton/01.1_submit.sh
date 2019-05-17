#!/bin/bash

[ -d submit ] || mkdir submit

NFILE=5
for MODE in ElElEl MuElEl ElMuMu MuMuMu; do
    for FILELIST in NanoAOD/2016/RD.Run2016/*/*.txt; do
        NJOBS=`cat $FILELIST | xargs -n$NFILE | wc -l`; NJOBS=`cat $FILELIST | xargs -n$NFILE | wc -l`
        JOBNAME=$MODE.`basename $FILELIST | sed -e 's;.txt;;g'`
        cd submit
        create-batch bash ../01_prod_ntuple.sh $MODE ../$FILELIST $NFILE --jobName $JOBNAME -T --nJobs $NJOBS
        cd ..
    done

    for FILELIST in NanoAOD/2016/MC.RunIISummer16.*/*/*.txt; do
        NJOBS=`cat $FILELIST | xargs -n$NFILE | wc -l`; NJOBS=`cat $FILELIST | xargs -n$NFILE | wc -l`
        JOBNAME=$MODE.`basename $FILELIST | sed -e 's;.txt;;g'`
        cd submit
        create-batch bash ../01_prod_ntuple.sh $MODE ../$FILELIST $NFILE --jobName $JOBNAME -T --nJobs $NJOBS
        cd ..
    done
done
