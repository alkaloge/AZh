#!/bin/bash

npar=$#
if [ $npar -ne 1 ]; then
    echo 
    echo Execute script with one parameter 
    echo available options : 2016, 2017, 2018, em, et, mt, tt and Run2
    echo Examples :
    echo ./RunGoF_Closure.bash Run2 
    echo ./RunGoF_Closure.bash tt
    echo
    exit
fi
sample=$1
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
    echo invalid argument : $1
    echo available options : 2016, 2017, 2018, em, et, mt, tt anf Run2
    echo
    exit
fi

folder=${CMSSW_BASE}/src/AZh/combine/ClosureTest/${sample}
outdir=${CMSSW_BASE}/src/AZh/combine/GoF_ClosureTest_${sample}

if [ ! -d "$outdir" ]; then
    echo making folder GoF_ClosureTest_${sample}
    mkdir $outdir
    cd $outdir
else 
    cd $outdir
    rm *
fi
combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --fixedSignalStrength 0 -m 300 --algo saturated -n .obs
for i in {1..100}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --toysFreq -m 300 --algo saturated -n .exp -t 10 -s ${random} --fixedSignalStrength 0  --job-mode condor --task-name gof.${random} --sub-opts='+JobFlavour = "workday"' 
done
cd -
