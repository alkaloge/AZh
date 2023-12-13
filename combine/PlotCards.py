#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
import ROOT
import os
        
############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Check datacards")
    parser.add_argument('-analysis','--analysis',dest='analysis',default='HIG18023')
    parser.add_argument('-year','--year',dest='year',default='2016')
    parser.add_argument('-cat','--cat',dest='cat',default='0btag')
    parser.add_argument('-channel','--channel',dest='chan',default='mmtt')
    parser.add_argument('-mass','--mass',dest='mass',default='400')
    parser.add_argument('-indir','--indir',dest='indir',default='datacards')
    parser.add_argument('-blind','--blind',dest='blind',default='yes')
    parser.add_argument('-xmin','--xmin',dest='xmin',default='200')
    parser.add_argument('-xmax','--xmax',dest='xmax',default='2000')
    parser.add_argument('-logx','--logx',dest='logx',default='yes')
    args = parser.parse_args()

    analysis = args.analysis
    year = args.year
    cat = args.cat
    channel = args.chan
    mass = args.mass
    prefix = ''
    group = utils.azh_groupbkgs
    bkgs = utils.azh_bkgs
    xmin = args.xmin
    xmax = args.xmax
    signals = {}

    blind = True
    if args.blind=='no' or args.blind=='No':
        blind = False
    
    logx = True
    if args.logx=='no' or args.logx=='No':
        blind = False

    folder = utils.BaseFolder+'/root_files'
    filename = 'MC_data_'+cat+'_'+year+'.root'
    filename_signal = 'signal_'+mass+'_'+cat+'_'+year+'.root'
    dirname = channel+'/'

    hig18023 = False

    if analysis=='root' or analysis=='Root' or analysis=='root':
        signals['ggA']='ggA'
        signals['bbA']='bbA'
    elif analysis=='azh' or analysis=='AZh':
        folder = utils.BaseFolder+'/'+indir'/Run2/'+mass
        filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
        filename_signal = filename
        signals['bbA']='bbA'+mass
        signals['ggA']='ggA'+mass
    elif analysis=='hig18023' or analysis=='HIG18023':
        hig18023 = True
        folder = utils.BaseFolder+'/HIG-18-023/datacards/'+utils.hig18023_channels[channel]+'/Aconstr_HsvFit90/common'
        filename = 'SR.input.root'
        filename_signal = filename
        signals['ggA']='AZH'+mass
        bkgs = utils.hig18023_bkgs
        group = utils.hig18023_groupbkgs
        prefix = 'x_'
        dirname = ''

    fullfilename = folder+'/'+filename
    fullfilename_signal = folder+'/'+filename_signal
    inputfile = ROOT.TFile(fullfilename)
    if inputfile==None:
        print('file %s not found'%(fullfilename))
        exit(1)
    inputfile_signal = ROOT.TFile(fullfilename_signal)
    if inputfile_signal==None:
        print('file %s not found'%(fullfilename_signal))
        exit(1)

    print('%s  %s  %s  '%(year,cat,channel))

    hists_bkg = {} 
    print
    for bkg in bkgs:
        hists_bkg[bkg] = inputfile.Get(dirname+prefix+bkg)
        sumofweights = hists_bkg[bkg].GetSumOfWeights()
        print('%11s %6.3f'%(bkg,sumofweights))

    hists = utils.GroupBackgrounds(hists_bkg,group)
    name = 'total'
    sumofweights = hists['tot_bkg'].GetSumOfWeights()
    print('%11s %6.3f'%(name,sumofweights))

    print
    for sig in signals:
        hists[sig] = inputfile_signal.Get(dirname+prefix+signals[sig])
        sigmass = sig+mass
        sumofweights = hists[sig].GetSumOfWeights()
        print('%11s %6.3f'%(sigmass,sumofweights))
    
    print
    hists['data'] = inputfile.Get(dirname+prefix+'data_obs')
    name='data'
    sumofweights = hists['data'].GetSumOfWeights()
    print('%11s %6.3f'%(name,sumofweights))
    print
    utils.Plot(hists,analysis=analysis,year=year,cat=cat,channel=channel,mass=mass,blind=blind,xmin=xmin,xmax=xmax,logx=logx)
