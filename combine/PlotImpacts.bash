#!/bin/bash
PROC=$1
MASS=$2
TYPE=$3
DIR=${TYPE}_impacts_${PROC}${MASS}
if [ ! -d "$DIR" ]; then
    echo directory does not exist : $DIR
    exit
fi
cd $DIR
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/${MASS}/ws.root --redefineSignalPOIs r_${PROC} -m ${MASS} -o impacts.json
plotImpacts.py -i impacts.json -o impacts
cd -
