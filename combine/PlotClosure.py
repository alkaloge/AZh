#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
import math
import ROOT
import os
from array import array

def AddHisto(hist1,hist2):
    nbins = hist1.GetNbinsX()
    for ib in range(1,nbins+1):
        x = hist1.GetBinContent(ib)
        ex = hist1.GetBinError(ib)
        y = hist2.GetBinContent(ib)
        ey =  hist2.GetBinError(ib)
        hist1.SetBinContent(ib,x+y)
        err = math.sqrt(ex*ex+ey*ey)
        hist1.SetBinError(ib,err)

def Plot(**kwargs):

    channel = kwargs.get('channel','mt')
    preFit  = kwargs.get('preFit',True)
    indir   = kwargs.get('indir','SS_lowstat')
    gof     = kwargs.get('gof',True)
    
    fit = not gof

    folder = 'shapes_fit_b'
    postfix = 'fit'
    if preFit:
        folder = 'shapes_prefit'
        postfix = 'prefit'

    reffile = ROOT.TFile(indir+'/Run2/azh_closure_2018_SS_'+channel+'.root')
    refhist = reffile.Get('%s/data_obs'%(channel))
    rootfile = ROOT.TFile(indir+'/fit.root')

    h_data = refhist.Clone('h_data')
    h_reducible = refhist.Clone('h_reducible')
    h_irreducible = refhist.Clone('h_irreducible')

    nbins = refhist.GetNbinsX()

    for ibin in range(1,nbins+1):
        h_data.SetBinContent(ibin,0.);
        h_data.SetBinError(ibin,0.);
        h_reducible.SetBinContent(ibin,0.);
        h_reducible.SetBinError(ibin,0.);
        h_irreducible.SetBinContent(ibin,0.);
        h_irreducible.SetBinError(ibin,0.);

    reducible_name = 'reducible'
    if fit:
        reducible_name = 'sig_'+channel

    for year in ['2016','2017','2018']:
        fileEra = ROOT.TFile(indir+'/Run2/azh_closure_'+year+'_SS_'+channel+'.root')
        hist_data = fileEra.Get(channel+'/data_obs')
        hist_reducible = rootfile.Get(folder+'/azh_closure_'+year+'_SS_'+channel+'/'+reducible_name)
        hist_irreducible = rootfile.Get(folder+'/azh_closure_'+year+'_SS_'+channel+'/irreducible')
        AddHisto(h_data,hist_data)
        AddHisto(h_reducible,hist_reducible)
        AddHisto(h_irreducible,hist_irreducible)
        
    data = h_data.Clone('h_data')
    reducible = h_reducible.Clone('h_reducible')
    irreducible = h_irreducible.Clone('h_irreducible')
    reducible.Add(reducible,irreducible)
    h_tot = reducible.Clone('h_tot')

    styles.InitData(data,"m(4l) [GeV]","Events")
    styles.InitHist(reducible,"m(4l) [GeV]","Events",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(irreducible,"m(4l) [GeV]","Events",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitTotalHist(h_tot)

    utils.zeroBinErrors(reducible)
    utils.zeroBinErrors(irreducible)
    ymax = 0
    nbins = data.GetNbinsX()
    xdata = []
    ydata = []
    xeldata = []
    xehdata = []
    yeldata = []
    yehdata = []
    for ib in range(1,nbins+1):
        x = data.GetBinContent(ib)
        err = data.GetBinError(ib)
        position = data.GetBinCenter(ib)
        xdata.append(position)
        xeldata.append(0.)
        xehdata.append(0.)
        ylow = -0.5 + math.sqrt(x+0.25)
        yhigh = 0.5 + math.sqrt(x+0.25)
        ydata.append(x)
        yeldata.append(ylow)
        yehdata.append(yhigh)
        xsum = x+err
        if xsum>ymax: ymax = xsum

    if h_tot.GetMaximum()>ymax: 
        ymax = h_tot.GetMaximum()

    reducible.GetYaxis().SetRangeUser(0.,1.2*ymax)
    reducible.GetXaxis().SetNdivisions(505)
    reducible.GetXaxis().SetNoExponent()
    reducible.GetXaxis().SetMoreLogLabels()

    dataGraph = ROOT.TGraphAsymmErrors(nbins,
                                       array('d',list(xdata)),
                                       array('d',list(ydata)),
                                       array('d',list(xeldata)),
                                       array('d',list(xehdata)),
                                       array('d',list(yeldata)),
                                       array('d',list(yehdata)))

    dataGraph.SetMarkerStyle(20)
    dataGraph.SetMarkerSize(1.6)

    canv_name = 'canv_'+year+'_'+channel
    canv = styles.MakeCanvas('canv','',500,500) 
    reducible.Draw('h')
    irreducible.Draw('hsame')
    h_tot.Draw('e2same')
    dataGraph.Draw('epsame')

    leg = ROOT.TLegend(0.67,0.55,0.9,0.8)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(styles.chan_map[channel])
    leg.AddEntry(data,'data','lp')
    leg.AddEntry(reducible,'reducible','f')
    leg.AddEntry(irreducible,'irreducible','f')
    leg.Draw()

    styles.CMS_label(canv,era="Run2",extraText="Preliminary")

    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print('figures/'+indir+'_'+channel+'_'+postfix+'.png')

parser = argparse.ArgumentParser(description="Check cards")
parser.add_argument('-channel','--channel',dest='chan',required=True)
parser.add_argument('-prefit','--prefit',action='store_true')
parser.add_argument('-folder','--folder',required=True)
parser.add_argument('-gof_option','--gof_option',dest='gof',action='store_true')

args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
styles.InitROOT()
styles.SetStyle()

Plot(channel=args.chan,preFit=args.prefit,indir=args.folder,gof=args.gof)


