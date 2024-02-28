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

def PlotSS(rootfile,**kwargs):

    bins = [199,240,280,320,360,400,550,700,2400]
    nbins = len(bins)-1

    channel = kwargs.get('channel','mt')
    preFit  = kwargs.get('preFit',True)
    
    folder = 'shapes_fit_b'
    postfix = 'fit'
    if preFit:
        folder = 'shapes_prefit'
        postfix = 'prefit'

    h_data = ROOT.TH1D('h_data','h_data',nbins,array('d',list(bins)))
    h_reducible = ROOT.TH1D('h_reducible','h_reducible',nbins,array('d',list(bins)))
    h_irreducible = ROOT.TH1D('h_irreducible','h_irreducible',nbins,array('d',list(bins)))

    print(h_data,h_reducible,h_irreducible)
    for year in ['2016','2017','2018']:
        fileEra = ROOT.TFile('ClosureTest/'+channel+'/azh_closure_'+year+'_SS_'+channel+'.root')
        hist_data = fileEra.Get(channel+'/data_obs')
        hist_reducible = rootfile.Get(folder+'/azh_closure_'+year+'_SS_'+channel+'/reducible')
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

    leg = ROOT.TLegend(0.65,0.45,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(styles.chan_map[channel])
    leg.AddEntry(data,'data','lp')
    leg.AddEntry(reducible,'reducible','f')
    leg.AddEntry(irreducible,'irreducible','f')
    leg.Draw()

    styles.CMS_label(canv,era=year)

    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print('figures/SS_closure_'+channel+'_'+postfix+'.png')



parser = argparse.ArgumentParser(description="Check cards")
parser.add_argument('-chan','--chan',dest='chan',required=True)
parser.add_argument('-postfit','--postfit',action='store_true')

args = parser.parse_args()

ROOT.gROOT.SetBatch(True)
styles.InitROOT()
styles.SetStyle()

rootfile = ROOT.TFile('ClosureTest/fit_closure.root')
PlotSS(rootfile,channel=args.chan,preFit=True)


