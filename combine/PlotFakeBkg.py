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
    cat = kwargs.get('cat','comb')
    channel = kwargs.get('channel','tt')
    charge  = kwargs.get('charge','OS')
    h_model   = hists['model']
    h_relaxed = hists['relaxed']
    h_prompt = hists['prompt']

    utils.fixNegativeBins(h_model)
    utils.fixNegativeBins(h_relaxed)

    styles.InitData(h_model,"m(4l) [GeV]","Events")
    styles.InitModel(h_relaxed,ROOT.kBlue,1)

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
        x_prompt = h_prompt.GetBinContent(ib)
        e_prompt = h_prompt.GetBinError(ib)
        print('[%4i,%4i]  %5.2f+/-%4.2f  |  %5.2f+/-%4.2f  |  %5.2f+/-%4.2f'%(low,high,x_model,e_model,x_relax,e_relax,x_prompt,e_prompt))
        y_model = x_model+e_model
        if y_model>ymax: ymax = y_model
        y_relax = x_relax+e_relax
        if y_relax>ymax: ymax = y_relax

    norm_model =  h_model.GetSumOfWeights()
    norm_relaxed = h_relaxed.GetSumOfWeights()
    ratio = norm_model/norm_relaxed
    h_relaxed.Scale(ratio)

    h_model.GetYaxis().SetRangeUser(0.,1.2*ymax)
    h_model.GetXaxis().SetNdivisions(505)
    h_model.GetXaxis().SetMoreLogLabels()
    h_model.GetXaxis().SetNoExponent()

    prob = h_model.KolmogorovTest(h_relaxed)
    prob_reverse = h_relaxed.KolmogorovTest(h_model)
    label_prob = 'prob(KS) = %4.2f'%(prob)
    label_reverse = 'prob(KS,reverse) = %4.2f'%(prob_reverse)

#    h_model.GetYaxis().SetRangeUser(0.005,10*h_model.GetMaximum())

    canv = styles.MakeCanvas("canv","",600,600)

    h_model.Draw('e1')
    h_relaxed.Draw('hsame')

    legTit = '%s %s'%(charge,styles.chan_map[channel])
    leg = ROOT.TLegend(0.65,0.6,0.9,0.8)
    styles.SetLegendStyle(leg)
    leg.SetHeader(legTit)
    leg.SetTextSize(0.04)
    leg.AddEntry(h_model,"FF estimate","ep")
    leg.AddEntry(h_relaxed,"relaxed ID","el")
    leg.Draw()
    styles.CMS_label(canv,era=year,extraText='Internal')

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)    
    latex.SetTextSize(0.045)
    if year=='Run2':
        latex.DrawLatex(0.6,0.4,label_prob)

    canv.SetLogx(True)
 #   canv.SetLogy(True)
    canv.RedrawAxis()
    canv.Update()
    canv.Print('figures/Fakes_%s_%s_%s_%s.png'%(year,cat,channel,charge))

    
    print('')
    print(label_prob)
    print(label_reverse)
    print('')




############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Plot reducible background")
    parser.add_argument('-year','--year',dest='year',required=True,help="""year : 2016, 2017, 2018 or Run2""",choices=['2016','2017','2018','Run2'])
    parser.add_argument('-channel','--channel',dest='channel',required=True,help=""" channel : em, et, mt, tt""",choices=['em','et','mt','tt'])
    parser.add_argument('-cat','--cat',dest='cat',required=True,help=""" category : 0btag, btag, comb """,choices=['0btag','btag','comb'])
    parser.add_argument('-same_sign','--same_sign',dest='ss',action='store_true',help=""" SS sideband""")
    parser.add_argument('-coarse','--coarse',dest='coarse',action='store_true')
    parser.add_argument('-folder','--folder',dest='folder',default='tighten_mtt_bin5GeV')
    args = parser.parse_args()

    bins = [199,240,280,320,360,400,450,550,700,1000,2400]
    if args.coarse:
        bins = [199,300,400,2400]

    histnames=['reducible','irreducible','ss_relaxed']
    year = args.year
    channel = args.channel
    cat = args.cat
    charge='OS'
    folder = args.folder
    if args.ss: 
        charge='SS'
        print
        print('Same sign region -> cat is set to \'comb\'')
        print
        cat='comb'
        histnames.append('ss_application')
        histnames.append('data')
    else:
        histnames.append('os_application')
        
    print
    print('      %s  %s  %s  %s '%(year,cat,channel,charge))
    print
    filename = 'root_files/%s/%s_%s_m4l_cons_%s_%s.root'%(folder,channel,cat,charge,year)
    print(filename)
    print
    rootfile = ROOT.TFile(filename)
    hists = {}
    histbase = rootfile.Get('reducible')
    nbins = histbase.GetNbinsX()
    for ib in range(1,nbins+1):
        xlower = int(histbase.GetBinLowEdge(ib))
        xupper = int(histbase.GetBinLowEdge(ib+1))
        print('[%4i,%4i]'%(xlower,xupper))
    print('')

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
    histosToPlot['prompt'] = utils.rebinHisto(hists['irreducible'],bins,'prompt')

    ComparePlots(histosToPlot,year=year,cat=cat,channel=channel,charge=charge)

