#!/bin/bash
year=$1
mass=$2
folder=${CMSSW_BASE}/src/AZh/combine/datacards/${year}/${mass}
jobdir=${CMSSW_BASE}/src/AZh/combine/jobs
cd GoF
rm *
combineTool.py -M GoodnessOfFit -d ${folder}/ws.root -m ${mass} --setParameters --algo saturated -n .obs
for i in {1..5}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --toysFreq -m ${mass} --algo saturated -n .exp -t 2 -s ${random} --job-mode condor --task-name exp.${random} --sub-opts='+JobFlavour = "workday"' 
done
cd -
