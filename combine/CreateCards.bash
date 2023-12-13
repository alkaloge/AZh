#!/bin/bash

cats=(btag 0btag)
masses=(225 275 300 325 350 375 400 450 500 600 700 800 900 1000 1200 1400 1600 1800 2000)
years=(2016 2017 2018)
for year in ${years[@]}
do
    for mass in ${masses[@]}
    do
	for cat in ${cats[@]}
	do
	    echo year : ${year}  --  category : ${cat}  --   mass : ${mass} 
	    ./make_datacards.py --year ${year} --btag ${cat} --mass ${mass}
	done
    done
done  
