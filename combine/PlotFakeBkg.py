#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
from array import array
import numpy as np
import ROOT
import os

def ComparePlots(hists,**kwargs):

    year = kwargs.get('year','2018')
    btag = kwargs.get('btag','0btag')
    channel = kwargs.get('channel','tt')
    charge  = kwargs.get('charge','OS')

    h_model   = hists['model']
    h_relaxed = hists['relaxed']

    utils.fixNegativeBins(h_model)
    utils.fixNegativeBins(h_relaxed)


    styles.InitData(h_model,"m(4l) [GeV]","Events")
    styles.InitData(h_relaxed,"m(4l) [GeV]","Events")
    h_relaxed.SetMarkerSize(1.2)
    h_relaxed.SetMarkerColor(ROOT.kBlue)
    h_relaxed.SetLineColor(ROOT.kBlue)


    nbins = h_model.GetNbinsX()
    ymax = 0
    print
    for ib in range(1,nbins+1):
        low = h_model.GetBinLowEdge(ib)
        high = h_model.GetBinLowEdge(ib+1)
        x_model = h_model.GetBinContent(ib)
        e_model = h_model.GetBinError(ib)
        x_relax = h_relaxed.GetBinContent(ib)
        e_relax = h_relaxed.GetBinError(ib)
        print('[%4i,%4i]  %5.2f+/-%4.2f  |  %5.2f+/-%4.2f'%(low,high,x_model,e_model,x_relax,e_relax))
        y_model = x_model+e_model
        if y_model>ymax: ymax = y_model
        y_relax = x_relax+e_relax
        if y_relax>ymax: ymax = y_relax

    h_model.GetYaxis().SetRangeUser(0.,1.2*ymax)

    canv = styles.MakeCanvas("canv","",600,600)

    h_model.Draw('h')
    h_relaxed.Draw('hsame')

    legTit = '%s %s %s'%(btag,channel,charge)
    leg = ROOT.TLegend(0.65,0.65,0.9,0.85)
    styles.SetLegendStyle(leg)
    leg.SetHeader(legTit)
    leg.SetTextSize(0.045)
    leg.AddEntry(h_model,"Model","ep")
    leg.AddEntry(h_model,"Relaxed","ep")
    leg.Draw()
    styles.CMS_label(canv,era=year,extraText='Internal')
    canv.SetLogx(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print('figures/%s_%s_%s_%s'%(year,btag,channel,charge))

############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Check datacards")
    parser.add_argument('-year','--year',dest='year',required=True,choices=utils.years,help="""year : 2016, 2017 or 2018""")
    parser.add_argument('-channel','--channel',dest='channel',required=True,choices=['em','et','mt','tt'],help=""" channel : em, et, mt and tt""")
    parser.add_argument('-btag','--btag',dest='btag',action='store_true',help=""" btag category """)
    parser.add_argument('-same_sign','--same_sign',dest='ss',action='store_true',help=""" SS sideband""")
    args = parser.parse_args()

    bins = [200,300,550,2000]

    histnames=['reducible','irreducible','ss_relaxed']
    year = args.year
    channel = args.channel
    btag='0'
    btag_leg = '0btag'
    if args.btag: 
        btag='1'
        btag_leg = 'btag'

    charge='OS'
    if args.ss: 
        charge='SS'
        histnames.append('ss_application')
        histnames.append('data')
    else:
        histnames.append('os_application')
        
    print
    print('      %s %sbtag  %s  %s '%(year,btag,channel,charge))
    print
    filename = 'root_files/%s_%s_m4l_cons_%s_%s.root'%(channel,btag,charge,year)
    print(filename)
    print
    rootfile = ROOT.TFile(filename)
    hists = {}
    for histname in histnames:
        hists[histname] = rootfile.Get(histname)
        norm,err = utils.getNormError(hists[histname])
        sumofweights = hists[histname].GetSumOfWeights()
        print('%15s  %7.4f +/- %7.4f --- %7.4f'%(histname,norm,err,sumofweights))
    
    print
    print('binning ->')
    nbins = hists['reducible'].GetNbinsX()
    for ib in range(1,nbins+1):
        low = hists['reducible'].GetBinLowEdge(ib)
        high = hists['reducible'].GetBinLowEdge(ib+1)
        print('[%4i,%4i]'%(low,high))
    print

    histosToPlot = {}
    if args.ss:
        histosToPlot['model'] = utils.rebinHisto(hists['ss_application'],bins,'model')
    else:
        histosToPlot['model'] = utils.rebinHisto(hists['os_application'],bins,'model')
    
    histosToPlot['relaxed'] = utils.rebinHisto(hists['reducible'],bins,'relaxed')

    ComparePlots(histosToPlot,year=year,btag=btag_leg,channel=channel,charge=charge)

