#!/bin/bash

channel=( "TTZct TTZut STZct STZut" )
mode=( "ElElEl MuElEl ElMuMu MuMuMu" )

for ch in ${channel[@]}; do
    for mo in ${mode[@]}; do
        nohup python TMVAEvaluation_btagWeight.py ${ch} ${mo} > log_eval_${ch}_${mo}_btagWeight.txt &
    done
done

