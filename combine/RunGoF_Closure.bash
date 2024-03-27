#!/bin/bash

npar=$#
if [ $npar -ne 2 ]; then
    echo 
    echo Execute script with three parameters 
    echo first argument : folder with datacards for closure test
    echo second argument : 2016, 2017, 2018, em, et, mt, tt and Run2
    echo Examples :
    echo ./RunGoF_Closure.bash closure Run2
    echo ./RunGoF_Closure.bash closure et
    echo
    exit
fi

folder=$1
sample=$2

if [ ! -d "$folder" ]; then
    echo folder $1 does not exist
    echo first create this folder with datacards for closure test
    exit
fi

count=0
list=(2016 2017 2018 em et mt tt Run2)
for i in ${list[@]} 
do
    if [ $sample = $i ]; then
	count=`expr $count + 1`
	break 
    fi
done

if [ $count -eq 0 ]; then
    echo
    echo invalid argument : $2
    echo available options : 2016, 2017, 2018, em, et, mt, tt anf Run2
    echo
    exit
fi

inputdir=${CMSSW_BASE}/src/AZh/combine/${folder}/${sample}
outdir=${CMSSW_BASE}/src/AZh/combine/GoF_${folder}_${sample}

if [ ! -d "$outdir" ]; then
    echo making folder ${outdir}
    mkdir ${outdir}
    cd $outdir
else 
    cd $outdir
    rm *
fi
combineTool.py -M GoodnessOfFit -d ${inputdir}/ws.root --fixedSignalStrength 0 -m 300 --algo saturated -n .obs
for i in {1..25}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit -d ${inputdir}/ws.root --toysFreq -m 300 --algo saturated -n .exp -t 40 -s ${random} --fixedSignalStrength 0  --job-mode condor --task-name gof.${random} --sub-opts='+JobFlavour = "workday"' 
done
cd -
