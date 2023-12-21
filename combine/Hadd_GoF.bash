#!/bin/bash
# $1 : ws = channel [tt,em,mt,et]
# $2 : algo = (saturated, KS, AD)
ws=${1}
algo=${2}
cd GoF/
mv higgsCombine.Closure_${ws}_${algo}.obs.GoodnessOfFit.mH125.root gof_Closure_${ws}_${algo}.obs.root
rm gof_${ws}_${algo}.exp.root 
hadd gof_Closure_${ws}_${algo}.exp.root higgsCombine.Closure_${ws}_${algo}_*.exp.GoodnessOfFit.mH125.*.root
rm higgsCombine.Closure_${ws}_${algo}_*.exp.GoodnessOfFit.mH125.*.root
cd -
