#!/usr/bin/env python

import ROOT
import os
import argparse
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch
import uproot


uncs_bins = {
    'bin1' : (  0, 400,0.10),
    'bin2' : (400, 700,0.10),
    'bin3' : (700,2500,0.10),
}

def getUnc(x):
    unc = 0
    if x<400: unc = 0.10
    elif x<700: unc = 0.10
    else: unc = 0.10
    return unc

def PlotSys(chan,hists,sysName):


    hist = hists['reducible_'+sysName+'Up'].Clone('Central')
    histUp = hists['reducible_'+sysName+'Up'].Clone('Up')
    histDown = hists['reducible_'+sysName+'Down'].Clone('Down')
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        x = hists['reducible'].GetBinContent(ib)
        e = hists['reducible'].GetBinError(ib)
        hist.SetBinContent(ib,x)
        hist.SetBinError(ib,e)

    styles.InitData(hist)
    styles.InitData(histUp)
    styles.InitData(histDown)

    histUp.SetMarkerSize(0)
    histUp.SetLineColor(1)
    histUp.SetMarkerColor(1)
    histUp.SetLineStyle(1)

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
    leg.SetHeader(chan+':'+sysName)
    leg.AddEntry(hist,'central','lp')
    leg.AddEntry(histUp,'Up','l')
    leg.AddEntry(histDown,'Down','l')
    leg.Draw()

    canv.SetLogx(True)
    canv.Update()
    canv.Print("figures/SS_systematics_%s_%s.png"%(chan,sysName))
    del canv

    print
    print
    print('Channel',chan,'uncertainty',sysName)
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        xup = histUp.GetBinContent(i)
        xdown = histDown.GetBinContent(i)
        low = hist.GetBinLowEdge(i)
        high = hist.GetBinLowEdge(i+1)
        print('[%4i,%4i]   %7.5f   %7.5f   %7.5f'%(int(low),int(high),x,xup,xdown))
    print
    print
    

def Plot(chan,hists):
    data = hists['data_obs'].Clone('h_data')
    reducible = hists['reducible'].Clone('h_reducible')
    irreducible = hists['irreducible'].Clone('h_irreducible')
    reducible.Add(reducible,irreducible)
    h_tot = reducible.Clone('h_tot')

    styles.InitData(data)
    data.SetLineColor(1)
    styles.InitHist(reducible,"","",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(irreducible,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitTotalHist(h_tot)

    utils.zeroBinErrors(reducible)
    utils.zeroBinErrors(irreducible)
    ymax = 0
    nbins = data.GetNbinsX()
    for ib in range(1,nbins+1):
        x = data.GetBinContent(ib)
        err = data.GetBinError(ib)
        xsum = x+err
        if xsum>ymax: ymax = xsum

    if h_tot.GetMaximum()>ymax: 
        ymax = h_tot.GetMaximum()

    data.GetXaxis().SetLabelSize(0.05)
    data.GetYaxis().SetLabelSize(0.05)
    data.GetXaxis().SetTitleOffset(1.0)
    data.GetYaxis().SetTitleOffset(1.2)
    data.GetXaxis().SetTitleSize(0.06)
    data.GetYaxis().SetTitleSize(0.06)
    
    data.GetXaxis().SetTitle('m(ll#tau#tau) (GeV)')
    data.GetYaxis().SetTitle('Events / bin')

    canv = styles.MakeCanvas('canv','',500,500) 
    data.Draw('e1')
    reducible.Draw('hsame')
    irreducible.Draw('hsame')
    h_tot.Draw('e2same')
    data.Draw('e1same')

    leg = ROOT.TLegend(0.65,0.45,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(styles.chan_map[chan]+' channel')
    leg.AddEntry(data,'data','lp')
    leg.AddEntry(reducible,'reducible','f')
    leg.AddEntry(irreducible,'irreducible','f')
    leg.Draw()
    styles.CMS_label(canv,era='Run2')
    canv.SetLogx(True)
    canv.Update()
    canv.Print('figures/SS_closure_'+chan+'.png')
    del canv

def quasiSignal(hist):
    hist_sig = hist.Clone('sig')
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        hist_sig.SetBinContent(ib,0.001)
        hist_sig.SetBinError(ib,0.0001)    
    return hist_sig


def setReducibleUncertainty(chan,hist):
    print 
    print('creating systematic templates of reducible background',chan)
    hists = {}
    nbins = hist.GetNbinsX()
    nameWithUnc = hist.GetName()+'_withUnc'
    histWithUnc = hist.Clone(nameWithUnc)
    for unc in uncs_bins:
        ntuple = uncs_bins[unc]
        nameUp = hist.GetName()+'_'+chan+'_'+unc+'Up'
        histUp = hist.Clone(nameUp)
        nameDown = hist.GetName()+'_'+chan+'_'+unc+'Down'
        histDown = hist.Clone(nameDown)        
        for ib in range(1,nbins+1):
            x = hist.GetBinContent(ib)
            centre = hist.GetBinCenter(ib)
            xup = x
            xdown = x
            if centre>ntuple[0] and centre<ntuple[1]:
                xup = x*(1.0 + ntuple[2])
                xdown = x/(1.0 + ntuple[2])
            histUp.SetBinContent(ib,xup)
            histDown.SetBinContent(ib,xdown)
        hists[nameUp] = histUp
        hists[nameDown] = histDown
        print

#    for ib in range(1,nbins+1):
#        x = hist.GetBinContent(ib)
#        center = hist.GetBinCenter(ib)
#        uncert = x*getUnc(center)
#        histWithUnc.SetBinContent(ib,x)
#        histWithUnc.SetBinError(ib,uncert)

    print

    hists[nameWithUnc] = histWithUnc
    return hists
                

def saveRooTFile(chan,hists,rootfile):
    rootfile.mkdir(chan)
    rootfile.cd(chan)
    for hist in hists:
        hists[hist].Write(hist)

def fixNegativeBins(hists):
    for namehist in hists:
        hist = hists[namehist]
        nbins = hist.GetNbinsX()
        for ib in range(1,nbins+1):
            x = hist.GetBinContent(ib)
            if x<0:
                hist.SetBinContent(ib,0.)
                hist.SetBinError(ib,0.)


def makedatacards(chan,rootfile):
    hists = {}
    foldername=os.getenv('CMSSW_BASE')+'/src/AZh/combine/root_files'
    inputfilename=foldername+'/'+chan+'_0_m4l_cons_SS.root'
    inputrootfile=ROOT.TFile(inputfilename)
    data = inputrootfile.Get('data')
    reducible = inputrootfile.Get('reducible')
    irreducible = inputrootfile.Get('irreducible')
    hists['data_obs'] = data
    hists['reducible'] = reducible
    hists['irreducible'] = irreducible
    fixNegativeBins(hists)
    hists['sig'] = quasiSignal(irreducible)
    hists_reducible = setReducibleUncertainty(chan,reducible)
    for hist in hists_reducible:
        hists[hist] = hists_reducible[hist]

    saveRooTFile(chan,hists,rootfile)
    Plot(chan,hists)
    for unc in uncs_bins:
        uncert = chan + '_' + unc
        PlotSys(chan,hists,uncert)

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()
    filename = os.getenv('CMSSW_BASE')+'/src/AZh/combine/root_files/ss_closure.root'
    rootfile = ROOT.TFile(filename,'recreate')
    for chan in ['em','et','mt','tt']:
        makedatacards(chan,rootfile)
    rootfile.Close()

    cats = [
        (1,'em'),
        (2,'et'),
        (3,'mt'),
        (4,'tt')
    ]    

    uncbins = ['bin1','bin2','bin3']

    cb = ch.CombineHarvester()

    cb.AddObservations(['*'],['azh_closure'],['2018'],['SS'],cats)
    cb.AddProcesses(['*'],['azh_closure'],['2018'],['SS'],['sig'],cats,True)
    cb.AddProcesses(['*'],['azh_closure'],['2018'],['SS'],['reducible','irreducible'],cats,False)
    
    cb.cp().process(['irreducible']).AddSyst(cb,'norm_bkgs','lnN',ch.SystMap()(1.15))
    cb.cp().process(['sig']).AddSyst(cb,'norm_sig','lnN',ch.SystMap()(1.10))
    for cat in cats:
        ib = cat[0]
        ib_name = cat[1]
        for unc in uncs_bins:
            cb.cp().process(['reducible']).bin_id([ib]).AddSyst(cb,ib_name+'_'+unc,'shape',ch.SystMap()(1.0))

    cb.AddDatacardLineAtEnd("* autoMCStats 0")

    cb.cp().backgrounds().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    cb.cp().signals().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    
    os.system('rm -rf ClosureTest')
    writer = ch.CardWriter(
        "$TAG/$ANALYSIS_$CHANNEL_$BIN.txt",
        "$TAG/$ANALYSIS_$CHANNEL_$BIN.root")
    writer.SetWildcardMasses([])
    writer.SetVerbosity(0);
    writer.WriteCards('ClosureTest/all',cb)
    os.system('./CreateWorkspacesClosure.bash')
    print
    print
    print('Datacards for closure test of fake background model in the SS region have created...')
    print
