#!/bin/bash
# $1 = year (2016, 2017, 2018, Run2)
# $2 = masses
# $3 = folder (datacards)
year=$1
mass=$2
folder=$3
ulimit -s unlimited
if [ ! -d "${folder}/${year}/${mass}" ] ; then
    echo folder ${folder}/${year}/${mass} does not exist !
    exit
fi
if [ -f "${year}/${mass}/ws.root" ] ; then
    rm ${folder}/${year}/$mass/ws.root
fi
if [ -f "${year}/${mass}/combined.txt.cmb" ] ; then
    rm ${folder}/${year}/$mass/combined.txt.cmb
fi
combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/bbA$:r_bbA[0,-20,40]"' --PO '"map=^.*/ggA$:r_ggA[0,-20,40]"' -i ${folder}/${year}/${mass} -m ${mass}
