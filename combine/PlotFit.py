#!/usr/bin/env python3

import AZh.combine.utilsAZh as utils
import AZh.combine.stylesAZh as styles
import argparse
from array import array
import ROOT
import os

def ExtractHistoFromFit(hist,fitfile,**kwargs):

    fittype = kwargs.get('fittype','prefit')
    channel = kwargs.get('channel','mmtt')
    year = kwargs.get('year','2018')
    cat = kwargs.get('cat','0btag')
    mass = kwargs.get('mass','300')
    templ = kwargs.get('templ','ggA')
    
    histname = 'shapes_%s/azh_%s_%s_%s_%s/%s'%(fittype,year,cat,channel,mass,templ)
    try: 
        reference = fitfile.Get(histname)
    except RuntimeError:
        print('Histogram %s is not found in fitDiagnostics.Test.root')
        print('You have to run fit first and save shapes -> ./RunFit.py --saveShapes')
        exit()

    norm = reference.GetSumOfWeights()
    is_positive = norm>0.0
    nbins = reference.GetNbinsX()
    for ib in range(1,nbins+1):
        x = 0
        e = 0
        if is_positive:
            x = reference.GetBinContent(ib)
            e = reference.GetBinError(ib)
        hist.SetBinContent(ib,x)
        hist.SetBinError(ib,e)
        
############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Plotting final discriminants")
    parser.add_argument('-year','--year',dest='year',default='all',choices=['2016','2017','2018','all'])
    parser.add_argument('-cat','--cat',dest='cat',default='0btag',choices=['btag','0btag','all'])
    parser.add_argument('-channel','--channel',dest='channel',default='all',choices=['et','mt','tt','all'])
    parser.add_argument('-folder','--folder',dest='folder',default='datacards')
    parser.add_argument('-mass','--mass',dest='mass',required=True)
    parser.add_argument('-xmin','--xmin',dest='xmin',type=float,default=199.9)
    parser.add_argument('-xmax','--xmax',dest='xmax',type=float,default=1200.0)
    parser.add_argument('-ymin','--ymin',dest='ymin',type=float,default=0.)
    parser.add_argument('-ymax','--ymax',dest='ymax',type=float,default=3.3)
    parser.add_argument('-logx','--logx',dest='logx',action='store_true')
    parser.add_argument('-logy','--logy',dest='logy',action='store_true')
    parser.add_argument('-fittype','--fittype',dest='fittype',default='prefit',choices=['prefit','fit_b','fit_s'])
    parser.add_argument('-show_yield','--show_yield',dest='show_yield',action='store_true')
    parser.add_argument('-unblind','--unblind',dest='unblind',action='store_true')
    parser.add_argument('-plotSignal','--plotSignal',dest='plotSignal',action='store_true')
    args = parser.parse_args()

    blind = not args.unblind
    year = args.year
    cat = args.cat
    channel = args.channel
    mass = args.mass
    fittype = args.fittype
    logx = args.logx
    logy = args.logy

    xmin = args.xmin
    xmax = args.xmax
    ratiomin = args.ymin
    ratiomax = args.ymax

    show_yield = args.show_yield

    prefix = ''
    suffix = '_%s_%s_%s'%(year,cat,channel)
    group = utils.azh_groupbkgs
    bkgs = utils.azh_bkgs
    signals = {}

    years = []
    cats = []
    channels = []

    year_legend = year
    cat_legend = 'no-btag'
    if cat=='btag':
        cat_legend = 'btag'
    channel_legend = channel

    signals['bbA'] = 'bbA'+mass
    signals['ggA'] = 'ggA'+mass

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
        channels = utils.azh_channels_noem
        channel_legend=''
    elif channel.lower()=='em':
        channels = ['eeem','mmem']
    elif channel.lower()=='et':
        channels = ['eeet','mmet']
    elif channel.lower()=='mt':
        channels = ['eemt','mmmt']
    elif channel.lower()=='tt':
        channels = ['eett','mmtt']
    else:
        channels = [channel]
 
    templates = ['data','other_bkg','reducible_bkg','ZZ_bkg','tot_bkg','ggA','bbA']
    templates_bkg = ['other_bkg','reducible_bkg','ZZ_bkg']
    templates_sig = ['ggA','bbA']
    templates_totbkg = ['tot_bkg']
    templates_data = ['data']
        
    print()
    print('plotting macro ->')
    print
    print('years ',years)
    print('categories ',cats)
    print('channels ',channels)
    print('templates ',templates)
    print

    hists = {}
    isFirst = True

    inputfile, inputfile_s = utils.GetInputFiles(
        analysis='azh',
        year='2018',
        cat='0btag',
        channel='mmtt',
        folder=args.folder,
        mass=mass)

    # creating templates
    dirname = 'mmtt/'
    templHist = inputfile.Get(dirname+prefix+'ZZ')
    bins = []
    nbins = templHist.GetNbinsX()
    for ib in range(1,nbins+1):
        bins.append(float(templHist.GetBinLowEdge(ib)))

    bins.append(1200.)
        
    inputfile.Close()
    inputfile_s.Close()

    fitfilename = utils.BaseFolder + '/fit_'+year_legend+'_mA'+mass+'_obs/fitDiagnostics.Test.root'
    if not os.path.isfile(fitfilename): 
        print('input file %s does not exist'%(fitfilename))
        print('Run script ./RunFit.py --sample Run2 --mass [mass] --saveShapes -obs --batch')
        exit()
    
    fitfile = ROOT.TFile(fitfilename)
    if fitfile==None or fitfile.IsZombie():
        print('file %s not properly closed'%(fitfile))
        exit()

    print('')
    print('histogram binning')
    for ib in range(1,nbins+1):
        print('[%4i,%4i]'%(bins[ib-1],bins[ib]))
        
    for template in templates:
        hists[template] = ROOT.TH1D(template,'',nbins,array('d',list(bins)))

    print('')

    fractions = {
        'et' : 0,
        'mt' : 0,
        'tt' : 0
    }

    h_channel = {
        'eeet' : 'et',
        'mmet' : 'et',
        'eemt' : 'mt',
        'mmmt' : 'mt',
        'eett' : 'tt',
        'mmtt' : 'tt'
    }

    for year in years:
        for cat in cats:
            for channel in channels:        
        
                hists_x = {}
                suffix = '_%s_%s_%s'%(year,cat,channel)
                dirname = channel+'/'

                # open input files
                inputfile, inputfile_s = utils.GetInputFiles(
                    analysis='azh',
                    year=year,
                    cat=cat,
                    channel=channel,
                    folder=args.folder,
                    mass=mass)

                # extract backgrounds
                hists_bkg = {} 
                for bkg in bkgs:
                    hist_bkg = inputfile.Get(dirname+prefix+bkg)
                    ExtractHistoFromFit(hist_bkg,
                                        fitfile,
                                        fittype=fittype,
                                        channel=channel,
                                        year=year,
                                        cat=cat,
                                        templ=bkg,
                                        mass=mass)
                    hists_bkg[bkg] = hist_bkg.Clone(bkg+suffix)
                    sumofweights = hists_bkg[bkg].GetSumOfWeights()
                    print('%15s %6.2f'%(bkg,sumofweights))
                    if bkg=='reducible':
                        fractions[h_channel[channel]] += sumofweights

                # grouping backgrounds
                hists_grp = utils.GroupBackgrounds(hists_bkg,group)
                for grp in hists_grp:
                    hist_grp = hists_grp[grp]
                    hists_x[grp+suffix] = hist_grp.Clone(grp+suffix)
                    sumofweights = hists_x[grp+suffix].GetSumOfWeights()
                name = 'total'
                sumofweights = hists_x['tot_bkg'+suffix].GetSumOfWeights()
                print('----------------------')
                print('%15s %6.2f'%(name,sumofweights))

                print
                for sig in signals:
                    hist_sig = inputfile_s.Get(dirname+prefix+signals[sig])
                    if fittype=='fit_s':
                        ExtractHistoFromFit(hist_sig,
                                            fitfile,
                                            fittype=fittype,
                                            channel=channel,
                                            year=year,
                                            mass=mass,
                                            templ=sig,
                                            cat=cat)
                    hists_x[sig+suffix] = hist_sig.Clone(sig+suffix)
                    sigmass = sig+mass
                    sumofweights = hists_x[sig+suffix].GetSumOfWeights()
                    print('%15s %6.2f'%(sigmass,sumofweights))
    
                print
                hist_data = inputfile.Get(dirname+prefix+'data_obs')
                hists_x['data'+suffix] = hist_data.Clone('data'+suffix)
                sumofweights = hists_x['data'+suffix].GetSumOfWeights()
                name = 'data' 
                print('%15s %6.0f'%(name,sumofweights))
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


    scaleBR = 1000.*0.1*0.062 # scale to sigma x BR = 500 fb
    scale_ggA = scaleBR
    scale_bbA = scaleBR
#    if fittype=='prefit' or fittype=='fit_b':
#        scale_ggA = 500*scaleBR
#        scale_bbA = 500*scaleBR

    print('accumulated yields ')
    print

    for template in templates_bkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_totbkg:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_sig:
        sumofweights = scaleBR*hists[template].GetSumOfWeights()
        print('%15s %6.2f'%(template,sumofweights))
    print
    for template in templates_data:
        sumofweights = hists[template].GetSumOfWeights()
        print('%15s %6.0f'%(template,sumofweights))

    print('')


    utils.Plot(hists,
               fractions,
               analysis='azh',
               year=year_legend,
               cat=cat_legend,
               channel=channel_legend,
               mass=mass,
               blind=blind,
               xmin=xmin,
               xmax=xmax,
               ratiomin=ratiomin,
               ratiomax=ratiomax,
               scale_bbA=scale_bbA,
               scale_ggA=scale_ggA,
               logx=logx,
               logy=logy,
               fittype=fittype,
               show_yield=show_yield,
               plotSignal=args.plotSignal,
               postfix=fittype)

