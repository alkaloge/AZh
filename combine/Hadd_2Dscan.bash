#!/bin/bash
cd $1
if [[ -f "Scan_obs.root" ]]; then
    rm Scan_obs.root
fi
if [[ -f "Scan_exp.root" ]]; then
    rm Scan_exp.root
fi
hadd Scan_obs.root higgsCombine.2Dscan_obs.POINTS*root
hadd Scan_exp.root higgsCombine.2Dscan_exp.POINTS*root
cd -
