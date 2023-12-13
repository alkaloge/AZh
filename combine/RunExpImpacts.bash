#!/bin/bash
# $1 - channel
ulimit -s unlimited

YEAR=${1}
MASS=${2}
OUTDIR=exp_impacts_AZh_${YEAR}_${MASS}
if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
fi
cd $OUTDIR
rm *
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_ggA/${YEAR}/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin -10 --rMax 10 --robustFit 1 -t -1 --doInitialFit 
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_ggA/${YEAR}/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin -10 --rMax 10 --robustFit 1 -t -1 --job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 2 --doFits
cd -

