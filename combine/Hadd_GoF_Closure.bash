#!/bin/bash
# $1 : sample name 
# available options : 2016, 2017, 2018, em, et, mt, tt  
cd GoF_ClosureTest_${sample}
mv higgsCombine.obs.GoodnessOfFit.mH300.root gof_obs.root
hadd gof_exp.root higgsCombine.exp.GoodnessOfFit.*.root 
cd -
