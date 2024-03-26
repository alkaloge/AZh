#!/usr/bin/env python

import ROOT
import os
import argparse
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch

def PlotSS(rootfile,**kwargs):

    year = kwargs.get('year','Run2')
    channel = kwargs.get('channel','all')

    h_data = rootfile.Get(channel+'/data_obs')
    h_reducible = rootfile.Get(channel+'/reducible')
    h_irreducible = rootfile.Get(channel+'/irreducible')

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
    for ib in range(1,nbins+1):
        x = data.GetBinContent(ib)
        err = data.GetBinError(ib)
        xsum = x+err
        if xsum>ymax: ymax = xsum

    if h_tot.GetMaximum()>ymax: 
        ymax = h_tot.GetMaximum()

    reducible.GetYaxis().SetRangeUser(0.,1.2*ymax)
    reducible.GetXaxis().SetNdivisions(505)
    reducible.GetXaxis().SetNoExponent()
    reducible.GetXaxis().SetMoreLogLabels()


    canv_name = 'canv_'+year+'_'+channel
    canv = styles.MakeCanvas('canv','',500,500) 
    reducible.Draw('h')
    irreducible.Draw('hsame')
    h_tot.Draw('e2same')
    data.Draw('e1same')

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
    canv.Print('figures/SS_closure_'+channel+'_'+year+'.png')



def quasiSignal(hist):
    hist_sig = hist.Clone('sig')
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        hist_sig.SetBinContent(ib,0.0001)
        hist_sig.SetBinError(ib,0.00001)    
    return hist_sig


def setReducibleUncertainty(h_inputs,**kwargs):

    year=kwargs.get('year','2018')
    channel=kwargs.get('channel','et')
    print 
    print('systematics for reducible background in year %s and channel %s '%(year,channel))
    print

    hist_fake = h_inputs['reducible']
    hist_ss_app = h_inputs['ss_application']

    name='%s_%s'%(year,channel)
    hist_ss_app_rebin = utils.rebinHisto(hist_ss_app,utils.bins_fakes,name)
    hist_reducible_rebin = utils.rebinHisto(hist_fake,utils.bins_fakes,name)
    hist_sys=hist_ss_app_rebin.Clone('hist_sys'+name)
    nbins_sys=hist_sys.GetNbinsX()

    hists = {}
    lower_edge=hist_sys.GetBinLowEdge(1)
    upper_edge=hist_sys.GetBinLowEdge(nbins_sys+1)

    for ib in range(1,nbins_sys+1):
        error = hist_ss_app_rebin.GetBinError(ib)
        x_ss_app = hist_ss_app_rebin.GetBinContent(ib)
        x_reducible = hist_reducible_rebin.GetBinContent(ib)
        x_max = max(x_ss_app,x_reducible)
        maximal = max(x_max,error)
        sys=1.0
        if maximal>0:
            sys=error/maximal                            
        hist_sys.SetBinContent(ib,sys)
        hist_sys.SetBinError(ib,0.)
        binname='bin%1i'%(ib)
        hist_sys.GetXaxis().SetBinLabel(ib,binname)
        nameUp = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Up'
        nameDown = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Down'
        hists[nameUp] = hist_fake.Clone(nameUp)
        hists[nameDown] = hist_fake.Clone(nameDown)

    nbins=hist_fake.GetNbinsX()
    for ib in range(1,nbins+1):
        center=hist_fake.GetBinCenter(ib)
        x=hist_fake.GetBinContent(ib)
        bin_sys=hist_sys.FindBin(center)
        binname=hist_sys.GetXaxis().GetBinLabel(bin_sys)
        sys=hist_sys.GetBinContent(bin_sys)
        x_down=max(0.,x/(1.0+sys))
        x_up=max(0.,x*(1.0+sys))
        nameUp = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Up'
        nameDown = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Down'
        hists[nameDown].SetBinContent(ib,x_down)
        hists[nameUp].SetBinContent(ib,x_up)
        print('%s  %6.3f %6.3f %6.3f'%(binname,x,x_down,x_up))

    return hists                

def saveRooTFile(channel,hists,rootfile):
    rootfile.mkdir(channel)
    rootfile.cd(channel)
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


def makedatacards(rootfile,**kwargs):
    
    year = kwargs.get('year','2016')
    channel = kwargs.get('channel','tt')

    hists = {}
    inputfilename=utils.BaseFolder+'/root_files/'+channel+'_comb_m4l_cons_SS_'+year+'.root'
    inputrootfile=ROOT.TFile(inputfilename)
    data = inputrootfile.Get('data')
    reducible = inputrootfile.Get('reducible')
    irreducible = inputrootfile.Get('irreducible')
    ss_application = inputrootfile.Get('ss_application')
    hists['data_obs'] = data
    hists['sig_'+channel] = reducible
    hists['irreducible'] = irreducible
    fixNegativeBins(hists)
    histsR = {}
    histsR['ss_application'] = ss_application
    histsR['reducible'] = reducible
    hists_reducible = setReducibleUncertainty(histsR,year=year,channel=channel)
    for hist in hists_reducible:
        hists[hist] = hists_reducible[hist]

    saveRooTFile(channel,hists,rootfile)

############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()     

    parser = ArgumentParser()
    parser.add_argument('-lowstat','--lowstat',dest='lowstat',action='store_true')
    parser.add_argument('-all','-all',dest='all_channels',action='store_true')
    parser.add_argument('-rigid','--rigid',dest='rigid',action='store_true')
    args = parser.parse_args()

    if os.path.isdir('ClosureSignal'):
        os.system('rm -rf ClosureSignal')

    os.system('mkdir ClosureSignal')


    bins = utils.bins_fakes
    newbins = len(bins)-1
    fake_uncs = []
    for ib in range(1,newbins+1):
        fake_uncs.append('bin%1i'%(ib))

    channels = ['et','mt','tt']
    cats = [
        (1,'et'),
        (2,'mt'),
        (3,'tt')
    ]    
    if args.all_channels:
        channels.append('em')
        cats.append((4,'em'))

    for year in utils.years:
        filename = utils.BaseFolder+'/root_files/m4l_SS_'+year+'_signal.root'
        rootfile = ROOT.TFile(filename,'recreate')
        for channel in channels:
            makedatacards(rootfile,year=year,channel=channel)
        rootfile.Close()


        cb = ch.CombineHarvester()

        cb.AddObservations(['*'],['azh_closure'],[year],['SS'],cats)
        for cat in cats:
            binname = cat[1]
            cb.AddProcesses(['*'],['azh_closure'],[year],['SS'],['sig_'+binname],[cat],True)
        cb.AddProcesses(['*'],['azh_closure'],[year],['SS'],['irreducible'],cats,False)
    
        # conservative uncertainties
        cb.cp().process(['irreducible']).AddSyst(cb,'norm_bkgs','lnN',ch.SystMap()(1.15))

        for cat in cats:
            ib = cat[0]
            ib_name = cat[1]
            for unc in fake_uncs:
                cb.cp().process(['sig_'+ib_name]).AddSyst(cb,ib_name+'_'+unc+'_'+year,'shape',ch.SystMap()(1.0))

        #        cb.AddDatacardLineAtEnd("* autoMCStats 20")

        cb.cp().backgrounds().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        cb.cp().signals().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    

        writer = ch.CardWriter(
            "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN.txt",
            "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN.root")
        writer.SetWildcardMasses([])
        writer.SetVerbosity(0);
        writer.WriteCards('ClosureSignal/Run2',cb)
        writer.WriteCards('ClosureSignal/%s'%(year),cb)
        writer.WriteCards('ClosureSignal/$BIN',cb)
        print
        print
        print('Datacards is SS region for year %s created'%(year))
        print
    
    # merging files per one year
    for channel in channels:
        if os.path.isfile('ClosureSignal/azh_closure_Run2_SS_%s.root'%(channel)):
            command = 'rm ClosureSignal/azh_closure_Run2_SS_%s.root'%(channel)
            os.system(command)
        command = 'hadd ClosureSignal/azh_closure_Run2_SS_%s.root ClosureSignal/%s/*.root'%(channel,channel)
        os.system(command)
        rootfile = ROOT.TFile('ClosureSignal/azh_closure_Run2_SS_%s.root'%(channel))
        rootfile.Close()
        command = 'combineTool.py -M T2W -o "ws.root" -i ClosureSignal/%s '%(channel)
        os.system(command)

    command = 'combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -o "ws.root" --PO \'map=.*/sig_et:r_et[1,0,2]\' --PO \'map=.*/sig_em:r_em[1,0,2]\' --PO \'map=.*/sig_mt:r_mt[1,0,2]\' --PO \'map=.*/sig_tt:r_tt[1,0,2]\' -i ClosureSignal/Run2 '
    os.system(command)
