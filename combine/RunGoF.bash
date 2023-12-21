#!/bin/bash
folder=${CMSSW_BASE}/src/AZh/combine/datacards/Run2/300
jobdir=${CMSSW_BASE}/src/AZh/combine/jobs
#outdir=$2
#if [ ! -d "$outdir" ]; then
#    mkdir $outdir
#else 
cd GoF
#combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --setParameters r_ggA=1,r_bbA=0 -m 300 --algo saturated -n .test
for i in {1..2}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --toysFreq -m 300 --algo saturated -n .test_exp -t 10 -s ${random} --setParameters r_ggA=1,r_bbA=0 --job-mode condor --task-name gof.${random} --sub-opts='+JobFlavour = "workday"' 
done
cd -
