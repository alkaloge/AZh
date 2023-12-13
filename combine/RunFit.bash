#!/bin/bash
cards=$1
model=$2
dir=${model}/combined/cmb

combine -M FitDiagnostics --saveNormalizations --saveShapes --saveWithUncertainties --robustHesse 1 --rMin=-100 --rMax=100 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 -m 125 ${dir}/${cards}.txt -n _${model}_${cards} -v 5

#combineTool.py -M FitDiagnostics --robustHesse 1 --setParameters r_ggH=0,r_bbH=0 --freezeParameters r_bbH --setParameterRanges r_ggH=-50,100 --redefineSignalPOIs r_ggH --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 -m 80 -d ${dir}/${ws}.root -n _${ws}_mH80 -v2

#combine -M MultiDimFit --robustFit 1 --setParameters r_ggH=0,r_bbH=0 --setParameterRanges r_ggH=-500,500 --redefineSignalPOIs r_ggH --cminDefaultMinimizerTolerance 0.01 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 -m 80 -d ${dir}/ws_${channel}_${bin}_${era}_80.root -n _multiDim_${channel}_${bin}_${era}_mH80
cd -
