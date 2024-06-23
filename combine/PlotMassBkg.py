#!/usr/bin/env python

import ROOT
import os
import math
from argparse import ArgumentParser
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch
from array import array 

def Plot(hists,**kwargs):

    channel = kwargs.get('channel','tt')
    isBkg = kwargs.get('bkg',True)
    mass = kwargs.get('mass','250')

    hist_cons = hists['cons']
    hist_corr = hists['corr']
    hist_raw = hists['raw']

    styles.InitModel(hist_cons,ROOT.kGreen+1,1)
    styles.InitModel(hist_corr,ROOT.kOrange+1,1)
    styles.InitModel(hist_raw,ROOT.kAzure+2,1)

    utils.zeroBinErrors(hist_cons)
    utils.zeroBinErrors(hist_corr)
    utils.zeroBinErrors(hist_raw)

    ymax = hist_cons.GetMaximum()
    if hist_raw.GetMaximum()>ymax:
        ymax = hist_raw.GetMaximum()
    if hist_corr.GetMaximum()>ymax:
        ymax = hist_corr.GetMaximum()

    hist_cons.GetYaxis().SetRangeUser(0.,1.3*ymax)
    hist_cons.GetXaxis().SetNdivisions(505)
    hist_cons.GetXaxis().SetRangeUser(100,500)
    if isBkg:
        hist_cons.GetXaxis().SetRangeUser(200,500)
    hist_cons.GetXaxis().SetTitle('m_{ll#tau#tau} (GeV)')
    hist_cons.GetYaxis().SetTitle('Events / 20 GeV')

    canv = styles.MakeCanvas('canv','',500,500) 
    hist_cons.Draw('h')
    hist_corr.Draw('hsame')
    hist_raw.Draw('hsame')

    x1leg = 0.65
    x2leg = 0.90
    if not isBkg:
        if mass=='400':
            x1leg = 0.25
            x2leg = 0.50

    leg = ROOT.TLegend(x1leg,0.45,x2leg,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    title = 'ggA('+mass+')'
    if isBkg:
        title = 'bkg'
    leg.SetHeader(styles.chan_map[channel]+' : '+title)
    leg.AddEntry(hist_raw,'Visible','le1')
    leg.AddEntry(hist_corr,'Corrected','le1')
    leg.AddEntry(hist_cons,'Constrained','le1')
    leg.Draw()

    styles.CMS_label(canv,era='2018',extraText='Simulation')

    canv.RedrawAxis()
    canv.Update()
    outputname = 'm4l_reco_ggA'+mass
    if isBkg:
        outputname = 'm4l_reco_'+channel
    canv.Print('figures/'+outputname+'.png')

############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()     

    parser = ArgumentParser()
    parser.add_argument('-c','--channel',dest='channel',default='tt',choices=['et','mt','tt'])
    parser.add_argument('-m','--mass',dest='mass',default='250',choices=['250','300','400'])
    args = parser.parse_args()

    types = {
        'cons': 'Constrained',
        'corr': 'Corrected',
        'raw': 'Visible'
    }
    label = {
        'cons': 'Constrained',
        'corr': 'Corrected  ',
        'raw' : 'Visible    '
    }
    bkg_hists = {}
    sig_hists = {}

    for reco in types:
        filename = 'root_files/%s_0_m4l_%s_OS_2018.root'%(args.channel,reco)
        inputfile = ROOT.TFile(filename)
        hist_irreducible = inputfile.Get('irreducible')
        hist_reducible = inputfile.Get('reducible')
        bkg_hists[reco] = hist_irreducible.Clone('bkg_'+reco)
        bkg_hists[reco].Add(bkg_hists[reco],hist_reducible,1.,1.)
        bkg_hists[reco].SetDirectory(0)

    bins = []
    for ib in range(100,620,20):
        bins.append(ib)

    filename = 'root_files/m%s.root'%(args.mass)
    inputfile = ROOT.TFile(filename)
    for reco in types:
        name = types[reco]
        sig_hist = inputfile.Get(name)
        sig_hists[reco] = utils.rebinHisto(sig_hist,bins,'sig_'+reco)
        sig_hists[reco].SetDirectory(0)

    Plot(bkg_hists,channel=args.channel,bkg=True,mass=args.mass)
    Plot(sig_hists,channel=args.channel,bkg=False,mass=args.mass)

    # computing Q-estimator
    for reco in types:
        nbins = bkg_hists[reco].GetNbinsX()
        likelihood = 0
        for ib in range(1,16):
            sig = sig_hists[reco].GetBinContent(ib+5)
            bkg = bkg_hists[reco].GetBinContent(ib)
            likelihood += sig*ROOT.TMath.Log(1+sig/bkg)
            m1b = bkg_hists[reco].GetBinLowEdge(ib)
            m2b = bkg_hists[reco].GetBinLowEdge(ib+1)
            m1s = sig_hists[reco].GetBinLowEdge(ib+5)
            m2s = sig_hists[reco].GetBinLowEdge(ib+6)
            print('[%3.0f,%3.0f] [%3.0f,%3.0f] %5.3f %5.3f'%(m1b,m2b,m1s,m2s,sig,bkg))
        print("%s %5.2f"%(label[reco],likelihood))

