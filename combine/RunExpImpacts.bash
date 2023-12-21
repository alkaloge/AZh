#!/bin/bash
# $1 - process (ggA or bbA)
# $2 - mass
ulimit -s unlimited

PROC=$1
MASS=$2
rMin=$3
rMax=$4
OUTDIR=exp_impacts_${PROC}${MASS}
if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
else
    rm ${OUTDIR}/*
fi 
cd $OUTDIR
#combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_${PROC}/Run2/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin ${rMin} --rMax ${rMax} --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --doInitialFit 
#combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_${PROC}/Run2/${MASS}/ws.root -m ${MASS} --expectSignal 1 --rMin ${rMin} --rMax ${rMax} --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 4 --doFits
cd -
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/${MASS}/ws.root -m ${MASS} --redefineSignalPOIs r_${PROC} --setParameters r_ggA=0,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-10,10 --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --doInitialFit 
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/${MASS}/ws.root -m ${MASS} --redefineSignalPOIs r_${PROC} --setParameters r_ggA=0,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-10,10 --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 4 --doFits
cd -

