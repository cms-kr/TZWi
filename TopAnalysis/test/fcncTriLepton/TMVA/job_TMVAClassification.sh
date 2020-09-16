#!/bin/bash

channel=( "TTZct TTZut STZct STZut" )
#channel=( "STZct STZut" )
mode=( "ElElEl MuElEl ElMuMu MuMuMu" )

for ch in ${channel[@]}; do
    category=$(echo ${ch} | cut -c1-2)
    for mo in ${mode[@]}; do
        #nohup python TMVAClassification.py -C ${ch} -M ${mo} -m BDTG_${category} -o ${ch}_${mo}_WZ_ZZ_Tr7Te3 > log_${ch}_${mo}_WZ_ZZ_Tr7Te3.txt &
        nohup python TMVAClassification.py -C ${ch} -M ${mo} -m BDTG_${category} -o ${ch}_${mo}_tightjet > log_${ch}_${mo}_tightjet.txt &
    done
done
