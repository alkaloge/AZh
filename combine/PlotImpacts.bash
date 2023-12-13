#!/bin/bash
YEAR=${1}
MASS=${2}
DIR=exp_impacts_AZh_${YEAR}_${MASS}
if [ ! -d "$DIR" ]; then
    echo directory does not exist : $DIR
    exit
fi
cd $DIR
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_ggA/${YEAR}/${MASS}/ws.root -m ${MASS} -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cd -
