#!/bin/bash

cd $1
mv higgsCombine.obs.GoodnessOfFit.mH300.root gof_obs.root
hadd gof_exp.root higgsCombine.exp.GoodnessOfFit.mH300.*.root
cd -
