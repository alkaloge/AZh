#!/bin/bash
ulimit -s unlimited
combineTool.py -M MultiDimFit -m 300 --setParameterRanges r_bbA=-0.2,1.3:r_ggA=-1.0,1.0 ws.root --algo=grid --points=10000 -t -1 --setParameters r_bbA=0,r_ggA=0 --robustFit 1 --cminDefaultMinimizerTolerance 0.01 --cminDefaultMinimizerStrategy=0 --X-rtd MINIMIZER_analytic -n .2Dscan -v2  
