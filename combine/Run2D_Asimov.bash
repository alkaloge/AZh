#!/bin/bash
# 
datacard=$1
ulimit -s unlimited
combineTool.py -M MultiDimFit -m 125 --setParameterRanges r_qqH=0,2:r_ggH=-10,10 -d ${datacard}.root --algo=grid --points=2500 -t -1 --setParameters r_qqH=1,r_ggH=1 --robustFit 1 --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 --X-rtd MINIMIZER_analytic -n .${datacard} -v2  

