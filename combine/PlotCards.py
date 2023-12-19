#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
from array import array
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
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh')
    parser.add_argument('-year','--year',dest='year',default='2016')
    parser.add_argument('-cat','--cat',dest='cat',default='0btag')
    parser.add_argument('-channel','--channel',dest='channel',default='mmtt')
    parser.add_argument('-mass','--mass',dest='mass',default='300')
    parser.add_argument('-xmin','--xmin',dest='xmin',type=float,default=200)
    parser.add_argument('-xmax','--xmax',dest='xmax',type=float,default=1000)
    parser.add_argument('-logx','--logx',dest='logx',type=bool,default=True)
    parser.add_argument('-blind','--blind',dest='blind',type=bool,default=False)
    args = parser.parse_args()


    analysis = args.analysis
    year = args.year
    cat = args.cat
    channel = args.channel
    mass = args.mass
    
    xmin = args.xmin
    xmax = args.xmax

    prefix = ''
    suffix = '_%s_%s_%s'%(year,cat,channel)
    group = utils.azh_groupbkgs
    bkgs = utils.azh_bkgs
    signals = {}

    years = []
    cats = []
    channels = []

    year_legend = year
    cat_legend = cat
    channel_legend = channel

    if analysis.lower()=='hig18023':
        prefix = 'x_'
        bkgs = utils.hig18023_bkgs
        group = utils.hig18023_groupbkgs
        signals['ggA'] = 'AZH'+mass 
        cats = ['0btag']
        years = ['2016']
        cat_legend='0btag'
        year_legend='2016'
        if channel.lower()=='all':
            channels = utils.azh_channels
            channel_legend =''
        else:
            channels.append(channel)
            channel_legend=channel
    else:
        if analysis.lower()=='azh':
            signals['bbA'] = 'bbA'+mass
            signals['ggA'] = 'ggA'+mass
        else:
            signals['bbA'] = 'bbA'
            signals['ggA'] = 'ggA'
        if year=='all':
            years = utils.years
            year_legend='Run2'
        else:
            years = [year]
            year_legend=year
        if cat.lower()=='all':
            cats = utils.azh_cats
            cat_legend=''
        else:
            cats = [cat]
            cat_legend=cat
        if channel.lower()=='all':
            channels = utils.azh_channels
            channel_legend=''
        else:
            channels = [channel]
            channel_legend=channel

    blind = args.blind;
    logx = args.logx;

    templates = ['data','other_bkg','reducible_bkg','ZZ_bkg','tot_bkg','ggA']
    templates_bkg = ['other_bkg','reducible_bkg','ZZ_bkg']
    templates_sig = ['ggA']
    templates_totbkg = ['tot_bkg']
    templates_data = ['data']
    if analysis.lower()=='azh':
        templates.append('bbA')
        templates_sig.append('bbA')
        
    print
    print('plotting macro ->')
    print
    print('analysis = %s'%(analysis))
    print('years ',years)
    print('categories ',cats)
    print('channels ',channels)
    print('templates ',templates)
    print

    hists = {}
    isFirst = True

    inputfile, inputfile_s = utils.GetInputFiles(
        analysis=analysis,
        year='2016',
        cat='0btag',
        channel='mmtt',
        mass=mass)

    # creating templates
    dirname = 'mmtt/'
    if analysis.lower()=='hig18023':
        dirname = ''
    templHist = inputfile.Get(dirname+prefix+'ZZ')
    bins = []
    nbins = templHist.GetNbinsX()
    for ib in range(1,nbins+2):
        bins.append(float(templHist.GetBinLowEdge(ib)))

    inputfile.Close()
    inputfile_s.Close()
    
    print
    print('histogram binning')
    for ib in range(1,nbins+1):
        print('[%4i,%4i]'%(bins[ib-1],bins[ib]))
        
    for template in templates:
        hists[template] = ROOT.TH1D(template,'',nbins,array('d',list(bins)))

    print

    for year in years:
        for cat in cats:
            for channel in channels:        
        
                hists_x = {}
                suffix = '_%s_%s_%s'%(year,cat,channel)
                dirname = channel+'/'
                if analysis.lower()=='hig18023':
                    dirname = ''

                # open input files
                inputfile, inputfile_s = utils.GetInputFiles(
                    analysis=analysis,
                    year=year,
                    cat=cat,
                    channel=channel,
                    mass=mass)

                # extract backgrounds
                hists_bkg = {} 
                for bkg in bkgs:
                    hist_bkg = inputfile.Get(dirname+prefix+bkg)
                    hists_bkg[bkg] = hist_bkg.Clone(bkg+suffix)
                    sumofweights = hists_bkg[bkg].GetSumOfWeights()
                    print('%15s %6.3f'%(bkg,sumofweights))

                # grouping backgrounds
                hists_grp = utils.GroupBackgrounds(hists_bkg,group)
                for grp in hists_grp:
                    hist_grp = hists_grp[grp]
                    hists_x[grp+suffix] = hist_grp.Clone(grp+suffix)
                    sumofweights = hists_x[grp+suffix].GetSumOfWeights()
                name = 'total'
                sumofweights = hists_x['tot_bkg'+suffix].GetSumOfWeights()
                print('----------------------')
                print('%15s %6.3f'%(name,sumofweights))

                print
                for sig in signals:
                    hist_sig = inputfile_s.Get(dirname+prefix+signals[sig])
                    hists_x[sig+suffix] = hist_sig.Clone(sig+suffix)
                    sigmass = sig+mass
                    sumofweights = hists_x[sig+suffix].GetSumOfWeights()
                    print('%15s %6.3f'%(sigmass,sumofweights))
    
                print
                hist_data = inputfile.Get(dirname+prefix+'data_obs')
                hists_x['data'+suffix] = hist_data.Clone('data'+suffix)
                sumofweights = hists_x['data'+suffix].GetSumOfWeights()
                name = 'data' 
                print('%15s %6.3f'%(name,sumofweights))
                print

                for template in templates:
                    name = template+suffix
                    hist = hists_x[name]
                    histTempl=hists[template]
                    utils.addHistos(histTempl,hist)

                inputfile.Close()
                inputfile_s.Close()

                print
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print


    print('accumulated yields ')
    print

    for template in templates_bkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.3f'%(template,sumofweights))
    print
    for template in templates_totbkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.3f'%(template,sumofweights))
    print
    for template in templates_sig:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.3f'%(template,sumofweights))
    print
    for template in templates_data:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.3f'%(template,sumofweights))

    print
    utils.Plot(hists,
               analysis=analysis,
               year=year_legend,
               cat=cat_legend,
               channel=channel_legend,
               mass=mass,
               blind=blind,
               xmin=xmin,
               xmax=xmax,
               logx=logx)

