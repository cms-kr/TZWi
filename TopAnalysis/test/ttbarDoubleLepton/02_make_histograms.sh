#!/bin/bash

HISTSET=../../data/histogramming/ttbbDilepton.yaml

if [ -d ntuple/reco/Run2017 ]; then
    find ntuple/reco/Run2017 -name '*.root' | \
        xargs -n1 -P$(nproc) tzwi-makehistograms Run2017 $HISTSET
fi

if [ -d ntuple/reco/MC2017 ]; then
    find ntuple/reco/MC2017 -name '*.root' | \
        xargs -n1 -P$(nproc) tzwi-makehistograms MC2017 $HISTSET
fi
