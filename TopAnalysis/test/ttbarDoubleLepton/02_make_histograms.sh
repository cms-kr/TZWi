#!/bin/bash

HISTSET=../../data/histogramming/ttbbDilepton.yaml
export NPROOF=$(nproc)
#export NPROOF=8

if [ -d ntuple/reco/Run2017 ]; then
    for DIR in ntuple/reco/Run2017/*/MuMu; do
        tzwi-makehistograms Run2017 $HISTSET $DIR
    done
fi

if [ -d ntuple/reco/MC2017 ]; then
    for DIR in ntuple/reco/MC2017/*/MuMu; do
        tzwi-makehistograms MC2017 $HISTSET $DIR
    done
fi
