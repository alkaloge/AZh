#!/bin/bash
dir=$1
mass=$2
proc=$3
ulimit -s unlimited
for year in 2016 2017 2018
do
    for cat in btag 0btag 
    do
	./make_datacards.py --year ${year} --btag ${cat} --outdir ${dir} --proc ${proc}
    done
done
combineTool.py -M T2W -o "ws.root" -i ${CMSSW_BASE}/src/AZh/combine/${dir}/${year}/${mass} -m ${mass}
