#!/bin/bash
cd root_files
for chan in em et mt tt
do
    for year in 2016 2017 2018 Run2
    do
	for typ in raw corr cons
	do
	    for region in OS
	    do
		mv ${chan}_0_m4l_${typ}_${region}_${year}.root ${chan}_0btag_m4l_${typ}_${region}_${year}.root
		mv ${chan}_1_m4l_${typ}_${region}_${year}.root ${chan}_btag_m4l_${typ}_${region}_${year}.root
		
	    done 
	done
    done
done

cd -
