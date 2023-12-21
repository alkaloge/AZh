#!/bin/bash
masses=(220 240 260 280 300 350 400)
for mass in ${masses[@]}
do
    mv limits_hig18023/higgsCombine.hig18023_2016_ggA.AsymptoticLimits.mH${mass}.root limits_hig18023/higgsCombine.hig18023_2016_ggA.exp.AsymptoticLimits.mH${mass}.root    
done
