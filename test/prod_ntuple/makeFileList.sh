#!/bin/bash

## Make RunIISummer16 MC list
ERA="RunIISummer16MiniAODv2-PUMoriond17"
for i in /xrootd/store/group/nanoAOD/*/*$ERA*; do
    PD=`basename $(dirname $i)`
    SD=`basename $i | sed -e 's;run2_201.MC_NANO_;;g'`
    echo /$PD/$SD
    [ ! -d datasets/$ERA ] && mkdir -p datasets/$ERA
    find $i -name '*.root' | grep -v failed >> datasets/$ERA/dataset_${PD}_${SD}.txt
done

## Make Run2016 RD list
ERA=Run2016
for i in /xrootd/store/group/nanoAOD/*/*$ERA*; do
    PD=`basename $(dirname $i)`
    SD=`basename $i | sed -e 's;run2_201.RD_NANO_;;g'`
    echo /$PD/$SD
    [ ! -d datasets/$ERA ] && mkdir -p datasets/$ERA
    find $i -name '*.root' | grep -v 'failed' >> datasets/$ERA/dataset_${PD}_${SD}.txt
done

## Make Run2017 RD list
ERA=Run2017
for i in /xrootd/store/group/NanoAOD/*/*/*$ERA*; do
    PD=`basename $(dirname $i)`
    SD=`basename $i`
    echo /$PD/$SD
    [ ! -d datasets/$ERA ] && mkdir -p datasets/$ERA
    find $i -name '*.root' | grep -v 'failed' >> datasets/$ERA/dataset_${PD}_${SD}.txt
done
