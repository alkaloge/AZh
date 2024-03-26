#!/usr/bin/env python

import ROOT
import os
import math
import argparse

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-channel','--channel',dest='channel',required=True,choices=['tt','mt','et','em'])
    parser.add_argument('-category','--cat',dest='cat',required=True,choices=['0btag','btag','comb'])
    parser.add_argument('-year','--year',dest='year',required=True,choices=['2016','2017','2018','Run2'])
    parser.add_argument('-folder','--folder',dest='folder',required=True)
    args = parser.parse_args()
    chan = args.channel
    year = args.year
    cat = args.cat
    folder = args.folder

    histnames_SS = ['reducible','irreducible','data','ss_relaxed','ss_application']
    histnames_OS = ['reducible','irreducible','ss_relaxed','os_application']

    inputfile_OS = ROOT.TFile('root_files/'+folder+'/'+chan+'_'+cat+'_m4l_cons_OS_'+year+'.root')
    inputfile_cards = ROOT.TFile('root_files/'+folder+'/MC_'+cat+'_'+year+'.root')

    if args.cat=='comb':
        inputfile_SS = ROOT.TFile('root_files/'+folder+'/'+chan+'_'+cat+'_m4l_cons_SS_'+year+'.root')
        print('------------- SS Region ------------')
          
        for histname in histnames_SS:
            hist = inputfile_SS.Get(histname)
            tot = hist.GetSumOfWeights()
            err2 = 0
            nbins = hist.GetNbinsX()
            for ib in range(1,nbins+1):
                e = hist.GetBinError(ib)
                err2 += e*e
                err = math.sqrt(err2)
            print('%15s : %5.2f +/- %5.2f'%(histname,tot,err))


    print('')
    print('------------- OS Region ------------')
    for histname in histnames_OS:
        hist = inputfile_OS.Get(histname)
        tot = hist.GetSumOfWeights()
        err2 = 0
        nbins = hist.GetNbinsX()
        for ib in range(1,nbins+1):
            e = hist.GetBinError(ib)
            err2 += e*e
        err = math.sqrt(err2)
        percent = err/tot
        print('%15s : %5.2f +/- %5.2f : %5.3f'%(histname,tot,err,percent))

    print('')

    hist = inputfile_cards.Get('mm'+args.channel+'/reducible')
    hist_ee = inputfile_cards.Get('ee'+args.channel+'/reducible')
    hist.Add(hist,hist_ee)
    tot = hist.GetSumOfWeights()
    err2 = 0
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        e = hist.GetBinError(ib)
        err2 += e*e
    err = math.sqrt(err2)
    histname = 'cross check'
    print('%15s : %5.2f +/- %5.2f'%(histname,tot,err))
        
    
    print('')
