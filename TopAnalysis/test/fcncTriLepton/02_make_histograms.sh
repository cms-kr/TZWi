#!/bin/bash

HISTSET=../../data/histogramming/fcncTrilepton.yaml

if [ -d ntuple/reco/Run2016 ]; then
    find ntuple/reco/Run2016 -name '*.root' | \
        xargs -n1 -P$(nproc) tzwi-makehistograms Run2016 $HISTSET
fi

if [ -d ntuple/reco/MC2016 ]; then
    find ntuple/reco/MC2016 -name '*.root' | \
        xargs -n1 -P$(nproc) tzwi-makehistograms MC2016 $HISTSET
fi

