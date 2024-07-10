#!/bin/bash
sample=$1
proc=$2
mass=$3
folder=limits_cls
rm ${folder}/limit_${sample}_${proc}_${mass}.root
hadd ${folder}/limit_${sample}_${proc}_${mass}.root ${folder}/higgsCombine.azh_${sample}_${proc}.POINT.*.HybridNew.mH${mass}.*.root
