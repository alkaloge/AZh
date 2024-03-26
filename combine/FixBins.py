#!/usr/bin/env python

import ROOT
import os
import math
import argparse
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch

for typ in ['corr','raw','cons']:
    for year in ['2016','2017','2018']:
        bin_number = 
        if typ='corr':
        for channel in ['et']:
            inputfile = ROOT.TFile('root_files/SS_highstat/%s_comb_m4l_corr_SS_%s.root'%(channel,year),'update')
            hist = inputfile.Get('data')
            if year
            inputfile.Close()

os.system('rm root_files/SS_highstat/et_comb_m4l_cons_SS_Run2.root')
os.system('hadd root_files/SS_highstat/et_comb_m4l_cons_SS_Run2.root root_files/SS_highstat/et_comb_m4l_cons_SS_2016.root root_files//et_comb_m4l_cons_SS_2017.root root_files/et_comb_m4l_cons_SS_2018.root')

os.system('rm root_files/mt_comb_m4l_cons_SS_Run2.root')
os.system('hadd root_files/mt_comb_m4l_cons_SS_Run2.root root_files/mt_comb_m4l_cons_SS_2016.root root_files/mt_comb_m4l_cons_SS_2017.root root_files/mt_comb_m4l_cons_SS_2018.root')
