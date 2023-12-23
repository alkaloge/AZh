#!/bin/bash
sample=$1
folder=${CMSSW_BASE}/src/AZh/combine/ClosureTest/${sample}
mkdir GoF_ClosureTest_${sample}
cd GoF_ClosureTest_${sample}
combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --fixedSignalStrength -m 300 --algo saturated -n .obs
for i in {1..100}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --toysFreq -m 300 --algo saturated -n .exp -t 10 -s ${random} --fixedSignalStrength 0  --job-mode condor --task-name gof.${random} --sub-opts='+JobFlavour = "workday"' 
done
cd -
