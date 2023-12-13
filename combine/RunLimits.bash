#!/bin/bash
# $1 - dir
# $2 - era = 2016, 2017, 2018, combined
# $3 - channel = em, tt
dir=${1}
era=${2}
chan=${3}
datacarddir=${CMSSW_BASE}/src/CombineHarvester/bbHRun2Legacy/${dir}/${era}/cmb
combine -M AsymptoticLimits \
    --noFitAsimov \
    --rAbsAcc 0 \
    --rRelAcc 0.0005 \
    --rMin=0 --rMax=50 \
    -d ${datacarddir}/ws.root \
    -n ".${chan}_${era}" \
    -m 125 \
    --X-rtd MINIMIZER_analytic \
    --cminDefaultMinimizerStrategy 0 \
    --cminDefaultMinimizerTolerance 0.01 \
    -v 3
