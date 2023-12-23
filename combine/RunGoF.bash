#!/bin/bash
##########################################################
# definition of parameters to steer running of GoF tests #
##########################################################
year=Run2      # options : 2016, 2017, 2018, Run2
mA=300         # mass hypothesis
r_ggA=0        # signal strength of ggA process
r_bbA=0        # signal strength of bbA process
algo=saturated # test-statistics, options saturated, KS, AD 
njobs=100      # number of jobs 
ntoys=10       # number of toys per job

folder=${CMSSW_BASE}/src/AZh/combine/datacards/${year}/${mA} # folder with workspace
outdir=${CMSSW_BASE}/src/AZh/combine/GoF_${year}_mA${mA} # output folder

if [ ! -d "$outdir" ]; then
    echo creating folder ${outdir}
    mkdir ${outdir}
    cd ${outdir}
else
    cd ${outdir}
    rm * # removing old stuff
fi

combineTool.py -M GoodnessOfFit -d ${folder}/ws.root -m ${mA} --setParameters r_ggA=${r_ggA},r_bbA=${r_bbA} --algo ${algo} -n .obs
i=0
while [ $i -lt ${njobs} ]
do 
    random=$RANDOM
    echo running job $i with random seed $random
    combineTool.py -M GoodnessOfFit -d ${folder}/ws.root --toysFreq -m ${mA} --setParameters r_ggA=${r_ggA},r_bbA=${r_bbA} --algo ${algo} -n .exp -t ${ntoys} -s ${random} --job-mode condor --task-name exp.${random} --sub-opts='+JobFlavour = "workday"' 
    i=`expr $i + 1`
done
cd -
