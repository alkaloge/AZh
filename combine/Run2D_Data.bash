#!/bin/bash
# 
datacard=$1
ulimit -s unlimited
combineTool.py -M MultiDimFit -m 125 --setParameterRanges r_qqH=-1,3:r_ggH=-13,7 -d ${datacard}.root --algo=grid --points=10000 --robustFit 1 --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 --X-rtd MINIMIZER_analytic -n .${datacard} -v2  

