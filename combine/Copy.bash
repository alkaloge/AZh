#!/bin/bash
years=(2016 2017 2018 Run2)
masses=(225 275 300 325 350 375 400 450 500 600 700 800 900 1000 1200 1400 1600 1800 2000)
for mass in ${masses[@]}
do
    for year in ${years[@]}
    do
	mv limits/higgsCombine.azh_${year}_bbA.AsymptoticLimits.mH${mass}.root limits/higgsCombine.azh_${year}_bbA.exp.AsymptoticLimits.mH${mass}.root
	mv limits/higgsCombine.azh_${year}_ggA.AsymptoticLimits.mH${mass}.root limits/higgsCombine.azh_${year}_ggA.exp.AsymptoticLimits.mH${mass}.root
	
    done
done
