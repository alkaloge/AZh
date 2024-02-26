#!/bin/bash
year=${1}
folder=${CMSSW_BASE}/src/AZh/combine/root_files
currentDir=$PWD
cd ${folder}
for cat in btag 0btag
do
    if [ -f "MC_data_${cat}_${year}.root" ]; then
	rm MC_data_${cat}_${year}.root
    fi
    hadd MC_data_${cat}_${year}.root data_${cat}_${year}.root MC_${cat}_${year}.root
done 
cd ${currentDir}
