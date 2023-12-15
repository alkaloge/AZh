#!/bin/bash
PROC=${1}
MASS=${2}
TYPE=${3}
DIR=${TYPE}_impacts_AZh_${PROC}${MASS}
if [ ! -d "$DIR" ]; then
    echo directory does not exist : $DIR
    exit
fi
cd $DIR
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards_${PROC}/Run2/${MASS}/ws.root -m ${MASS} -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cd -
