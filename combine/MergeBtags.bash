#!/bin/bash
cd root_files
for chan in em et mt tt
do
    for btag in 0 1
    do
	for region in OS SS
	do
	    for typ in raw corr cons
	    do
		mv ${chan}_${btag}_m4l_${typ}_${region}_all-years.root ${chan}_${btag}_m4l_${typ}_${region}_Run2.root
	    done 
	done
    done
done
for year in 2016 2017 2018 Run2
do
    for chan in em et mt tt
    do
	for typ in raw corr cons
	do
	    for region in OS
	    do
		outfile=${chan}_m4l_${typ}_${region}_${year}.root 
		if [ -f "$outfile" ]; then
		    rm ${outfile}
		fi
		hadd ${chan}_m4l_${typ}_${region}_${year}.root ${chan}_0_m4l_${typ}_${region}_${year}.root ${chan}_1_m4l_${typ}_${region}_${year}.root
	    done
	done
    done
done
cd -
