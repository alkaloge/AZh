#!/usr/bin/env python

import stylesAZh as styles
import argparse
import ROOT
import os
unc = ['unclMET','tauID0','tauID1','tauID10','tauID11','tauES','efake','mfake','eleES','muES','pileup','l1prefire','eleSmear']

cat_map = {
    '1':'eeem',
    '2':'eeet',
    '3':'eemt',
    '4':'eett',
    '5':'mmem',
    '6':'mmet',
    '7':'mmmt',
    '8':'mmtt'
}

cats = ['btag','0btag']
channels = ['mmem','mmet','mmmt','mmtt','eeem','eeet','eemt','eett']
bkgds = [
    "ggZZ",
    "ZZ",
    "TTZ",
    "VVV",
    "ZHtt",
    "TTHtt",
    "ZHWW",
    "ggZHWW",
    "ggHZZ",
    "reducible"
]

parser = argparse.ArgumentParser(description="Check cards")
parser.add_argument('-chan','--chan',dest='chan',default='btag')
parser.add_argument('-cat','--cat',dest='cat',default='mmtt')
parser.add_argument('-year','--year',dest='year',default='2018')
parser.add_argument('-templ','--templ',dest='templ',default='data_obs')
parser.add_argument('-sys','--sys',dest='sys',default='')
parser.add_argument('-mass','--mass',dest='mass',default='1000')
args = parser.parse_args()


ROOT.gROOT.SetBatch(True)
styles.InitROOT()
styles.SetStyle()


binname = args.cat
folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/Run2/'+args.mass
filename = 'azh_'+args.year+'_'+args.chan+'_'+args.cat+'_'+args.mass+'.root'
fullfilename = folder+'/'+filename
inputfile = ROOT.TFile(fullfilename)
hist = inputfile.Get(binname+'/'+args.templ)
if hist==None:
    print('template %s not found in analysis bin %s'%(args.templ,binname))
    exit(1)

histUp = hist
histDown = hist
if args.sys!='':
    histUp = inputfile.Get(binname+'/'+args.templ+'_'+args.sys+'Up')
    histDown = inputfile.Get(binname+'/'+args.templ+'_'+args.sys+'Down')
    if histUp==None:
        print('template %s with systematics %s not found in analysis bin %s'%(args.templ,args.sys,binname))
        print('check content of file',fullfilename)
        exit(1)

print
print('Printing content of template %s of analysis bin %s and systematic %s'%(args.templ,binname,args.sys))
print
#      1  0.00073  0.00073  0.00073
print(' bin  central      up       down')
print('--------------------------------')
nbins = hist.GetNbinsX()
for i in range(1,nbins):
    x = hist.GetBinContent(i)
    xup = histUp.GetBinContent(i)
    xdown = histDown.GetBinContent(i)
    if args.sys=='':
        print(' %2i  %5.3f'%(i,x))
    else:
        print(' %2i   %7.5f   %7.5f   %7.5f'%(i,x,xup,xdown))

    
styles.InitData(hist)
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
if histUp.GetMaximum()>ymax: ymax = histUp.GetMaximum()
if histDown.GetMaximum()>ymax: ymax = histDown.GetMaximum()
hist.GetYaxis().SetRangeUser(0.,1.5*ymax)

canv = styles.MakeCanvas('canv','',500,500)
hist.Draw("e1")
histUp.Draw("hsame")
histDown.Draw("hsame")

leg = ROOT.TLegend(0.6,0.6,0.9,0.9)
styles.SetLegendStyle(leg)
leg.SetTextSize(0.045)
leg.SetHeader(args.year+" "+args.chan+"_"+args.cat)
leg.AddEntry(hist,args.templ,'lp')
leg.AddEntry(histUp,args.sys+'Up','l')
leg.AddEntry(histDown,args.sys+'Down','l')
leg.Draw()

canv.SetLogx(True)
canv.Update()
canv.Print("figures/%s_%s_%s_%s_%s.png"%(args.year,args.chan,cat_map[args.cat],args.templ,args.sys))

