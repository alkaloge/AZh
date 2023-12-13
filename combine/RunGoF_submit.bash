#!/bin/bash
# $1 : channel
# $2 : algo

channel=${1}
ws=ws
algo=${2}
dir=${CMSSW_BASE}/
inputdir=${dir}/output/cards/${channel}
outputdir=${CMSSW_BASE}/src/CombineHarvester/bbHRun2Legacy/GoF/

jobname=GoF_${channel}_${ws}_${algo}_obs
cat > ${dir}/jobs/${jobname}.sh <<EOF1
#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700
cd ${CMSSW_BASE}/src
cmsenv
cd ${outputdir}
ulimit -s unlimited
combine -M GoodnessOfFit -d ${inputdir}/${ws}.root -m 125 --algo ${algo} -n .${channel}_${algo}.obs
EOF1
chmod u+x ${dir}/jobs/${jobname}.sh
cat > ${dir}/jobs/${jobname}.submit << EOF2
+RequestRuntime=3000

RequestMemory = 2000

executable = ${dir}/jobs/${jobname}.sh

transfer_executable = True
universe            = vanilla
getenv              = True
Requirements        = OpSysAndVer == "CentOS7"

output              = ${dir}/jobs/${jobname}.out
error               = ${dir}/jobs/${jobname}.error
log                 = ${dir}/jobs/${jobname}.log

queue
EOF2
chmod u+x ${dir}/jobs/${jobname}.submit
condor_submit ${dir}/jobs/${jobname}.submit

for i in {1..50}
do
    jobname=GoF_${ws}_${channel}_${algo}_${i}
    random=$RANDOM
    cat > ${dir}/jobs/${jobname}.sh << EOF3
#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700
cd ${CMSSW_BASE}/src
cmsenv
cd ${outputdir}
ulimit -s unlimited
combine -M GoodnessOfFit -d ${inputdir}/${ws}.root --toysFreq -m 125 --algo ${algo} -n .${channel}_${algo}_${i}.exp -t 20 -s ${random}
EOF3
    chmod u+x ${dir}/jobs/${jobname}.sh
    cat > ${dir}/jobs/${jobname}.submit << EOF4
+RequestRuntime=6000

RequestMemory = 2000

executable = ${dir}/jobs/${jobname}.sh

transfer_executable = True
universe            = vanilla
getenv              = True
Requirements        = OpSysAndVer == "CentOS7"

output              = ${dir}/jobs/${jobname}.out
error               = ${dir}/jobs/${jobname}.error
log                 = ${dir}/jobs/${jobname}.log

queue
EOF4
    chmod u+x ${dir}/jobs/${jobname}.submit
    condor_submit ${dir}/jobs/${jobname}.submit
done

