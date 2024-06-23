#!/bin/bash
################################################################
#    definition of parameters to steer running of GoF tests    #
################################################################
sample=$1        # options : 2016, 2017, 2018, Run2, et, mt, tt
mA=250           # mass hypothesis
r_ggA=0          # signal strength of ggA process
r_bbA=0          # signal strength of bbA process
algo=saturated   # test-statistics, options saturated, KS, AD 
njobs=25         # number of jobs 
ntoys=40         # number of toys per job
folder=datacards # folder with datacards (e.g. datacards)

npar=$#
if [ $npar -ne 1 ]; then
    echo 
    echo Execute script with one parameter:
    echo 2016, 2017, 2018, em, et, mt, tt and Run2
    echo Examples :
    echo ./RunGoF.bash datacards Run2
    echo ./RunGoF.bash datacards et
    echo
    exit
fi


folder=${CMSSW_BASE}/src/AZh/combine/${folder}/${sample}/${mA} # folder with workspace
outdir=${CMSSW_BASE}/src/AZh/combine/GoF_${sample}_${mA} # output folder

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
