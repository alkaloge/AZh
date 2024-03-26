#!/bin/bash
mass=300
folder=datacards/Run2/${mass}

# Running fit with robustHesse (improved estimate of errors via covariance matrix)
combineTool.py -M FitDiagnostics --robustHesse 1 --setParameters r_ggA=0,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-20,20 --redefineSignalPOIs r_ggA --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 -m ${mass} -d ${folder}/ws.root -v2

# Running fit with robustFit (asymmetric errors on POI estimated from likelihood scan)
#combineTool.py -M FitDiagnostics --robustFit 1 --setParameters r_ggA=0,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-20,20 --redefineSignalPOIs r_ggA --cminDefaultMinimizerTolerance 0.05 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=1 -m ${mass} -d ${folder}/ws.root -v2
