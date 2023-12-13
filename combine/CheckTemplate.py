#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
import ROOT
import os

def plot(hists,**kwargs):

    hist = hists['central']
    histUp = hists['up']
    histDown = hists['down']

    analysis = kwargs.get('analysis','azh')

    year = kwargs.get('year','2016')
    cat = kwargs.get('cat','0btag')
    channel = kwargs.get('channel','mmtt')

    templ = kwargs.get('templ','data_obs')
    sys = kwargs.get('sys','')

    print
    print('%s'%(analysis))
    print('%s  %s  %s'%(year,channel,sys))
    print('%s  %s'%(templ,sys))
    print
    nbins = hist.GetNbinsX()

    if sys=='':
        print(' bin         value +/- stat. unc')
    else:
        print(' bin        central      up       down')
    
    print('--------------------------------')
    
    norm = 0
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        ex = hist.GetBinError(i)
        ilow = int(hist.GetBinLowEdge(i))
        ihigh = int(hist.GetBinLowEdge(i+1))
        norm += x
        if sys=='':
            print('[%4i,%4i]   %5.3f +/- %5.3f'%(ilow,ihigh,x,ex))
        else:
            xup = histUp.GetBinContent(i)
            xdown = histDown.GetBinContent(i)
            print('[%4i,%4i]   %7.5f   %7.5f   %7.5f'%(ilow,ihigh,x,xup,xdown))

    print('Overall yield = %7.4f (%7.4f)'%(hist.GetSum(),norm))
    
    styles.InitData(hist)
    if sys!='':
        styles.InitData(histUp)
        styles.InitData(histDown)
        histUp.SetMarkerSize(0)
        histUp.SetLineColor(2)
        histUp.SetMarkerColor(2)
        histUp.SetLineStyle(1)

        histDown.SetMarkerSize(0)
        histDown.SetLineColor(4)
        histDown.SetMarkerColor(4)
        histDown.SetLineStyle(1)

        styles.zeroBinErrors(histUp)
        styles.zeroBinErrors(histDown)

    ymax = hist.GetMaximum()
    if sys!='':
        if histUp.GetMaximum()>ymax: ymax = histUp.GetMaximum()
        if histDown.GetMaximum()>ymax: ymax = histDown.GetMaximum()
    hist.GetYaxis().SetRangeUser(0.,1.5*ymax)
    
    canv = styles.MakeCanvas('canv','',700,700)
    hist.Draw("e1")
    if sys!='':
        histUp.Draw("hsame")
        histDown.Draw("hsame")

    leg = ROOT.TLegend(0.5,0.5,0.8,0.8)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(year+" "+cat+"_"+channel)
    leg.AddEntry(hist,templ,'lp')
    leg.AddEntry(histUp,sys+'Up','l')
    leg.AddEntry(histDown,sys+'Down','l')
    leg.Draw()

    canv.SetLogx(True)
    canv.Update()
    if sys=='':
        canv.Print("figures/%s_%s_%s_%s_%s.png"%(analysis,year,cat,channel,templ))
    else:
        canv.Print("figures/%s_%s_%s_%s_%s_%s.png"%(analysis,year,cat,channel,templ,sys))


############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Check datacards")
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh')
    parser.add_argument('-year','--year',dest='year',default='2018')
    parser.add_argument('-cat','--cat',dest='cat',default='0btag')
    parser.add_argument('-channel','--channel',dest='chan',default='mmtt')
    parser.add_argument('-template','--template',dest='templ',default='all')
    parser.add_argument('-sys','--sys',dest='sys',default='unclMET_2018')
    parser.add_argument('-mass','--mass',dest='mass',default='300')
    args = parser.parse_args()

    rebin = False
    analysis = args.analysis
    year = args.year
    cat = args.cat
    channel = args.chan
    templ = args.templ
    sys = args.sys
    mass = args.mass

    folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/root_files'
    filename = 'MC_data_'+cat+'_'+year+'.root'
    dirname = channel+'/'
    prefix = ''
    
    templates = [templ]
    uncs = [sys]
    if sys in ['*','all','All']:
        uncs = utils.azh_uncs
    if templ in ['*','all','All']:
        templates = utils.azh_bkgs

    hig18023 = False

    if analysis=='azh' or analysis=='AZh':
        folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/datacards/Run2/'+mass
        filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
        for sig in utils.azh_signals:
            templates.append(sig+mass)
    elif analysis=='hig18023' or analysis=='HIG18023':
        hig18023 = True
        if sys in ['*','all','All']:
            uncs = utils.hig18023_uncs
        if templ in ['*','all','All']:
            templates = utils.azh_bkgs
        for sig in hig18023_signals:
            templates.append(sig+mass)
        folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/HIG-18-023/datacards/'+utils.hig18023_channels[channel]+'/Aconstr_HsvFit90/common'
        filename = 'SR.input.root'
        prefix = 'x_' 
        dirname = ''

    fullfilename = folder+'/'+filename
    inputfile = ROOT.TFile(fullfilename)
    if inputfile==None:
        print('file %s not found'%(fullfilename))
        exit(1)


    for template in templates:
        hist = inputfile.Get(dirname+prefix+template)
        if hist==None:
            print('template %s not found in folder %s'%(TemplToPass,dirname))
            break
        for unc in uncs:
            histUp = hist
            histDown = hist
            if unc!='':
                histUp = inputfile.Get(dirname+prefix+template+'_'+unc+'Up')
                histDown = inputfile.Get(dirname+prefix+template+'_'+unc+'Down')
            if histUp==None or histDown==None:
                print('template %s with systematics %s not found'%(templ,sys))
                break
            hists = {}
            if rebin:
                hists['central'] = utils.rebinHisto(hist,utils.newbins,'central')
                hists['up'] = utils.rebinHisto(histUp,utils.newbins,'up')
                hists['down'] = utils.rebinHisto(histDown,utils.newbins,'down')
            else:
                hists['central'] = hist
                hists['up'] = histUp
                hists['down'] = histDown
            plot(hists,analysis=analysis,year=year,cat=cat,channel=channel,templ=template,sys=unc)
