#!/usr/bin/env python

import ROOT
import os
import argparse
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-channel','--channel',required=True,choices=['tt','mt','et','em'])
    args = parser.parse_args()
    chan = args.channel
    histnames = ['reducible','irreducible','data']
    

    file1 = ROOT.TFile('root_files/'+chan+'_0_m4l_cons_SS.root')
    file2 = ROOT.TFile('root_files/'+chan+'_0_m4l_cons_SS_all-years.root')
    file3 = ROOT.TFile('root_files/ss_closure.root')

    print
    for histname in histnames:
        print
        print('------------------------------------------')
        print(histname)
        hist1 = file1.Get(histname)
        hist2 = file2.Get(histname)
        namehist = histname
        if histname=='data': namehist='data_obs'
        hist3 = file3.Get(chan+'/'+namehist)
        nbins = hist1.GetNbinsX()
        for ib in range(1,nbins+1):
            low = hist1.GetBinLowEdge(ib)
            high = hist1.GetBinLowEdge(ib)
            x1 = hist1.GetBinContent(ib)
            e1 = hist1.GetBinError(ib)
            x2 = hist2.GetBinContent(ib)
            e2 = hist2.GetBinError(ib)
            x3 = hist3.GetBinContent(ib)
            e3 = hist3.GetBinError(ib)
            print('[%4i,%4i] | %5.2f+/-%5.2f | %5.2f+/-%5.2f | %5.2f+/-%5.2f |'%(low,high,x1,e1,x2,e2,x3,e3))

    print('------------------------------------------')
    print
