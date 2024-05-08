#!/usr/bin/env python

import ROOT
import os
import math
from argparse import ArgumentParser
import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch
from array import array 

def PlotClosure(rootfile,**kwargs):

    year = kwargs.get('year','Run2')
    channel = kwargs.get('channel','all')
    typ = kwargs.get('typ','cons')
    fit = kwargs.get('fit',False)

    h_data = rootfile.Get(channel+'/data_obs')
    h_reducible = rootfile.Get(channel+'/reducible')
    h_irreducible = rootfile.Get(channel+'/irreducible')

    data = h_data.Clone('h_data')
    reducible = h_reducible.Clone('h_reducible')
    irreducible = h_irreducible.Clone('h_irreducible')
    reducible.Add(reducible,irreducible)
    h_tot = reducible.Clone('h_tot')

    xtit="m(4l) [GeV]"
    if typ=='corr':
        xtit="m(4l)^{corr} [GeV]"
    if typ=='raw':
        xtot="m(4l)^{raw} [GeV]"

    styles.InitData(data,xtit,"Events")
    styles.InitHist(reducible,xtit,"Events",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(irreducible,xtit,"Events",ROOT.TColor.GetColor("#FFCCFF"),1001)
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
    canv.Print('figures/m4l_'+typ+'_closure_'+channel+'_'+year+'.png')

def quasiSignal(hist):
    hist_sig = hist.Clone('sig')
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        hist_sig.SetBinContent(ib,0.0001)
        hist_sig.SetBinError(ib,0.00001)    
    return hist_sig


def setReducibleUncertainty(h_inputs,**kwargs):

    year = kwargs.get('year','2018')
    channel = kwargs.get('channel','et')
    typ = kwargs.get('typ','cons')
    lowstat = kwargs.get('lowstat',False)
    fit = kwargs.get('fit',False)

    bins_fakes = [150,300,400,2500]
    if typ=='raw':
        bins_fakes=[100,220,400,2500]
    elif typ=='corr':
        bins_fakes=[100,220,400,2500]
    
    if lowstat:
        bins_fakes = [150,320,450,2400]

    print 
    print('systematics for reducible background in year %s and channel %s '%(year,channel))
    print

    hist_fake = h_inputs['reducible']
    hist_sb_app = h_inputs['sb_application']

    print(hist_sb_app.GetNbinsX())

    name='%s_%s'%(year,channel)
    hist_sb_app_rebin = utils.rebinHisto(hist_sb_app,bins_fakes,name)
    hist_reducible_rebin = utils.rebinHisto(hist_fake,bins_fakes,name)
    hist_sys=hist_sb_app_rebin.Clone('hist_sys'+name)
    nbins_sys=hist_sys.GetNbinsX()

    hists = {}
    lower_edge=hist_sys.GetBinLowEdge(1)
    upper_edge=hist_sys.GetBinLowEdge(nbins_sys+1)

    for ib in range(1,nbins_sys+1):
        error = hist_sb_app_rebin.GetBinError(ib)
        x_sb_app = hist_sb_app_rebin.GetBinContent(ib)
        x_reducible = hist_reducible_rebin.GetBinContent(ib)
        x_max = max(x_sb_app,x_reducible)
        maximal = max(x_max,error)
        sys=1.0
        if maximal>0:
            sys=error/maximal                            
        hist_sys.SetBinContent(ib,sys)
        hist_sys.SetBinError(ib,0.)
        binname='bin%1i'%(ib)
        hist_sys.GetXaxis().SetBinLabel(ib,binname)
        nameUp = 'reducible_'+channel+'_'+binname+'_'+year+'Up'
        nameDown = 'reducible_'+channel+'_'+binname+'_'+year+'Down'
        if fit:
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
        nameUp = 'reducible_'+channel+'_'+binname+'_'+year+'Up'
        nameDown = 'reducible_'+channel+'_'+binname+'_'+year+'Down'
        if fit:
            nameUp = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Up'
            nameDown = 'sig_'+channel+'_'+channel+'_'+binname+'_'+year+'Down'
        hists[nameDown].SetBinContent(ib,x_down)
        hists[nameUp].SetBinContent(ib,x_up)
        low = hist_fake.GetXaxis().GetBinLowEdge(ib)
        up = hist_fake.GetXaxis().GetBinLowEdge(ib+1)
        print('%s_%s_%s : [%4i,%4i]'%(channel,binname,year,int(low),int(up)))

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
    
    year = kwargs.get('year','2018')
    channel = kwargs.get('channel','tt')
    typ = kwargs.get('typ','cons')    
    OS = kwargs.get('OS',False)
    lowstat = kwargs.get('lowstat',False)
    fit = kwargs.get('fit',False)

    bins = [150,200,250,300,350,400,450,500,550,600,650,700,750,800,900,1000,2500]
    if typ=='raw':
        bins = [100,140,180,220,260,300,350,400,450,500,600,800,1200]
    elif typ=='corr':
        bins = [150,220,260,300,350,400,450,500,600,800,1200]

    if lowstat:
        bins = [150,200,240,280,320,360,400,450,550,700,1000,2400]

    folder = 'SS_highstat'
    Sign = 'SS'
    sign = 'ss'
    if lowstat:
        folder = 'SS_reducible'
    if OS:
        folder = 'OS_lowmtt'
        Sign = 'OS'
        sign = 'os'

    hists = {}
    inputfilename=utils.BaseFolder+'/root_files/'+folder+'/'+channel+'_comb_m4l_'+typ+'_'+Sign+'_'+year+'.root'
    inputrootfile=ROOT.TFile(inputfilename)
    print(inputrootfile)

    data = inputrootfile.Get('data')
    reducible = inputrootfile.Get('reducible')
    irreducible = inputrootfile.Get('irreducible')
    sb_application = inputrootfile.Get(sign+'_application')
    hists['data_obs'] = utils.rebinHisto(data,bins,'data_obs')
    if channel=='tt':
        hists['data_obs'].SetBinContent(1,8.)
        hists['data_obs'].SetBinError(1,math.sqrt(8.))
        hists['data_obs'].SetBinContent(2,15.)
        hists['data_obs'].SetBinError(2,math.sqrt(15.))
    if channel=='et':
        hists['data_obs'].SetBinContent(1,5.)
        hists['data_obs'].SetBinError(1,math.sqrt(5.))
        hists['data_obs'].SetBinContent(2,6.)
        hists['data_obs'].SetBinError(2,math.sqrt(6.))
        hists['data_obs'].SetBinContent(5,2.)
        hists['data_obs'].SetBinError(5,math.sqrt(2.))
    if channel=='mt':
        hists['data_obs'].SetBinContent(1,6.)
        hists['data_obs'].SetBinError(1,math.sqrt(6.))
        hists['data_obs'].SetBinContent(2,9.)
        hists['data_obs'].SetBinError(2,math.sqrt(9.))
    if channel=='em':
        hists['data_obs'].SetBinContent(2,9.)
        hists['data_obs'].SetBinError(2,math.sqrt(9.))
        hists['data_obs'].SetBinContent(3,4.)
        hists['data_obs'].SetBinError(3,math.sqrt(4.))

    rebinned_reducible = utils.rebinHisto(reducible,bins,'reducible_rebinned')
    if fit:
        hists['sig_'+channel] = rebinned_reducible
    else:
        hists['reducible'] = utils.rebinHisto(reducible,bins,'sig_'+channel)
    hists['irreducible'] = utils.rebinHisto(irreducible,bins,'irreducible')
    fixNegativeBins(hists)
    hists['sig'] = quasiSignal(irreducible)
    histsR = {}
    histsR['sb_application'] = utils.rebinHisto(sb_application,bins,'rebinned_application')
    histsR['reducible'] = utils.rebinHisto(reducible,bins,'rebinned_reducible')
    hists_reducible = setReducibleUncertainty(histsR,year=year,channel=channel,typ=typ,lowstat=lowstat,fit=fit)
    for hist in hists_reducible:
        print(hist)
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
    parser.add_argument('-year','--year',dest='year',default='Run2',choices=['2016','2017','2018','Run2'])
    parser.add_argument('-type','--type',dest='typ',default='cons',choices=['cons','corr','raw'])
    parser.add_argument('-all','--all',dest='all_channels',action='store_true')
    parser.add_argument('-lowstat','--lowstat',dest='lowstat',action='store_true')
    parser.add_argument('-rigid','--rigid',dest='rigid',action='store_true')
    parser.add_argument('-outdir','--outdir',dest='outdir',required=True)
    parser.add_argument('-gof_option','--gof_option',dest='gof',action='store_true')
    parser.add_argument('-OS','--OS',dest='OS',action='store_true')
    args = parser.parse_args()

    fit = not args.gof

    isOS = args.OS

    channels = ['et','mt','tt']
    cats = [
        (1,'et'),
        (2,'mt'),
        (3,'tt')
    ]    
    if args.all_channels:
        cats.append((4,'em'))
        channels.append('em')

    pathname = utils.BaseFolder+'/'+args.outdir
        
    if os.path.isdir(pathname):
        os.system('rm -rf %s'%(pathname))

    os.system('mkdir %s'%(pathname))

    rigid = args.rigid
    typ = args.typ
    lowstat = args.lowstat
    if lowstat:
        typ = 'cons'

    fake_uncs = []
    for ib in range(1,4):
        fake_uncs.append('bin%1i'%(ib))

    years = []
    if args.year=='Run2':
        years = utils.years
    else:
        years.append(args.year)

    for year in years:
        filename = utils.BaseFolder+'/root_files/m4l_'+typ+'_SB_'+year+'.root'
        rootfile = ROOT.TFile(filename,'recreate')
        for channel in channels:
            makedatacards(rootfile,year=year,channel=channel,typ=typ,lowstat=lowstat,fit=fit,OS=isOS)
        rootfile.Close()

        cb = ch.CombineHarvester()

        cb.AddObservations(['*'],['azh_closure'],[year],['SB'],cats)
        if fit:
            for cat in cats:
                binname = cat[1]
                cb.AddProcesses(['*'],['azh_closure'],[year],['SB'],['sig_'+binname],[cat],True)
            cb.AddProcesses(['*'],['azh_closure'],[year],['SB'],['irreducible'],cats,False)
        else: 
            cb.AddProcesses(['*'],['azh_closure'],[year],['SB'],['sig'],cats,True)
            cb.AddProcesses(['*'],['azh_closure'],[year],['SB'],['reducible','irreducible'],cats,False)
    
        # conservative uncertainties
        cb.cp().process(['irreducible']).AddSyst(cb,'norm_bkgs','lnN',ch.SystMap()(1.20))
        cb.cp().process(['sig']).AddSyst(cb,'norm_sig','lnN',ch.SystMap()(1.10))

        if rigid: # assume 20%
            for cat in cats:
                ib = cat[0]
                ib_name = cat[1]
                if fit:
                    cb.cp().process(['sig_'+ib_name]).bin_id([ib]).AddSyst(cb,ib_name,'lnN',ch.SystMap()(1.20))
                else:
                    cb.cp().process(['reducible']).bin_id([ib]).AddSyst(cb,ib_name,'lnN',ch.SystMap()(1.20))
        else:
            for cat in cats:
                ib = cat[0]
                ib_name = cat[1]
                for unc in fake_uncs:
                    if fit:
                        cb.cp().process(['sig_'+ib_name]).bin_id([ib]).AddSyst(cb,ib_name+'_'+unc+'_'+year,'shape',ch.SystMap()(1.0))
                    else:
                        cb.cp().process(['reducible']).bin_id([ib]).AddSyst(cb,ib_name+'_'+unc+'_'+year,'shape',ch.SystMap()(1.0))

        cb.AddDatacardLineAtEnd("* autoMCStats 0")

        cb.cp().backgrounds().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
        cb.cp().signals().ExtractShapes(filename, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    

        writer = ch.CardWriter(
            "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN.txt",
            "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN.root")
        writer.SetWildcardMasses([])
        writer.SetVerbosity(0);
        writer.WriteCards('%s/Run2'%(pathname),cb)
        writer.WriteCards('%s/%s'%(pathname,year),cb)
        writer.WriteCards('%s/$BIN'%(pathname),cb)
        print
        print
        print('Datacards in SB region for year %s created'%(year))
        print
    
    # merging files per one year
    for channel in channels:
        if os.path.isfile('%s/azh_closure_Run2_%s.root'%(pathname,channel)):
            command = 'rm %s/azh_closure_Run2_%s.root'%(pathname,channel)
            os.system(command)
        command = 'hadd %s/azh_closure_Run2_%s.root %s/%s/*.root'%(pathname,channel,pathname,channel)
        os.system(command)
        if args.gof:
            rootfile = ROOT.TFile('%s/azh_closure_Run2_%s.root'%(pathname,channel))
            PlotClosure(rootfile,year=args.year,channel=channel,typ=typ)
            rootfile.Close()
        command = 'combineTool.py -M T2W -o "ws.root" -i %s/%s '%(pathname,channel)
        if fit:
            command = 'combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -o "ws.root" --PO \'map=.*/sig_et:r_et[1,0,2]\' --PO \'map=.*/sig_em:r_em[1,0,2]\' --PO \'map=.*/sig_mt:r_mt[1,0,2]\' --PO \'map=.*/sig_tt:r_tt[1,0,2]\' -i %s/%s '%(pathname,channel)
        os.system(command)
    command = 'combineTool.py -M T2W -o "ws.root" -i %s/Run2 '%(pathname)
    if fit:
        command = 'combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel -o "ws.root" --PO \'map=.*/sig_et:r_et[1,0,2]\' --PO \'map=.*/sig_em:r_em[1,0,2]\' --PO \'map=.*/sig_mt:r_mt[1,0,2]\' --PO \'map=.*/sig_tt:r_tt[1,0,2]\' -i %s/Run2 '%(pathname)
    os.system(command)
