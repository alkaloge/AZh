import ROOT 
import math
from array import array
import numpy as np
import os
import AZh.combine.stylesAZh as styles

#############################
##### General settings ######
#############################

#############################
##### working dir ###########
#############################
BaseFolder=os.getenv('CMSSW_BASE')+'/src/AZh/combine'

#######################
# folder  for figures #
#######################
FiguresFolder = BaseFolder+'/figures'

###################
#  luminosities   #
###################

eraLumi = {
    "UL2016" : 36300,
    "UL2016_postVFP" : 16800,
    "UL2016_preVFP"  : 19500,
    "UL2017" : 41480,    
    "UL2018" : 59830
}

#############################

years = ['2016','2017','2018']

variations = ["Up","Down"]

newbins = [200,220,240,260,280,300,320,340,360,380,400,700]

##############################
# AZh analysis : definitions # 
##############################

azh_masses = ['225','275','300','325','350','375','400','450','500','600','700','800','900','1000','1200','1400','1600','1800','2000']

azh_bkgs = [
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

azh_groupbkgs = {
    'reducible_bkg' : ['reducible'],
    'ZZ_bkg' : ['ZZ','ggZZ'],
    'other_bkg' : ['TTZ','VVV','ZHtt','TTHtt','ZHWW','ggZHWW','ggHZZ']
}

azh_signals = [
    'ggA',
    'bbA'
]

azh_cats = [
    'btag',
    '0btag'
]

azh_channels = [
    'eeem',
    'eeet',
    'eemt',
    'eett',
    'mmem',
    'mmet',
    'mmmt',
    'mmtt'
]

azh_channelmap = {
    '1':'eeem',
    '2':'eeet',
    '3':'eemt',
    '4':'eett',
    '5':'mmem',
    '6':'mmet',
    '7':'mmmt',
    '8':'mmtt'
}

azh_uncs = [
    'unclMET',
    'tauID0',
    'tauID1',
    'tauID10',
    'tauID11',
    'tauES',
    'efake',
    'mfake',
    'eleES',
    'muES',
    'pileup',
    'l1prefire',
    'eleSmear'
]

#####################################
# HIG-18-023 analysis : definitions # 
#####################################

hig18023_bkgs = [
    "ggZZ",
    "ZZ",
    "WH_htt125",
    "ZH_htt125",
    "ttHnonBB125",
    "triboson",
    "ttZ",
    "data_FR",
]

hig18023_groupbkgs = {
    'reducible_bkg' : ['data_FR'],
    'ZZ_bkg' : ['ZZ','ggZZ'],
    'other_bkg' : ['WH_htt125','ZH_htt125','ttHnonBB125','triboson','ttZ']
}

hig18023_signals = [
    "AZH"
]

hig18023_channels = {
    "eeem":"EEEM",
    "eeet":"EEET",
    "eemt":"EEMT",
    "eett":"EETT",
    "mmem":"MMEM",
    "mmet":"MMET",
    "mmmt":"MMMT",
    "mmtt":"MMTT"
}

hig18023_masses = ['220','240','260','280','300','350','400']

hig18023_unc = [
    'CMS_scale_t_1prong',
    'CMS_scale_t_1prong1pizero',
    'CMS_scale_t_3prong',
    'CMS_scale_met_unclustered',
    'CMS_scale_met_clustered'
]

#######################################
# Creating shape systematic templates #
#######################################
def ComputeSystematics(h_central, h_sys, name):
    h_up = h_central.Clone(name+"Up")
    h_down = h_central.Clone(name+"Down")
    nbins = h_central.GetNbinsX()
    for i in range(1,nbins+1):
        x_up = h_sys.GetBinContent(i)
        x_central = h_central.GetBinContent(i)
        x_down = x_central
        if x_up>0:
            x_down = x_central*x_central/x_up
        h_up.SetBinContent(i,x_up)
        h_down.SetBinContent(i,x_down)

    return h_up, h_down

def symmetrizeUnc(hists):
    hist = hists['central']
    histUp = hists['up']
    histDown = hists['down']
    if hist==None: 
        print('symmetrizeUnc : central histo is null')
        return
    if histUp==None: 
        print('symmetrizeUnc : upward histo is null')
        return
    if histDown==None: 
        print('symmetrizeUnc : downward histo is null')
        return
    nbins = hist.GetNbinsX()
    nbinsUp = histUp.GetNbinsX()
    nbinsDown = histDown.GetNbinsX()
    if nbins!=nbinsUp or nbins!=nbinsDown:
        print('symmetrizeUnc : inconsistency between number of bins (central/up/down)')

    for ib in range(1,nbins+1):
        delta = 0.5*(histUp.GetBinContent(ib)-histDown.GetBinContent(ib))
        up = hist.GetBinContent(ib) + delta
        down = hist.GetBinContent(ib) - delta
        histUp.SetBinContent(ib,up)
        histDown.SetBinContent(ib,down)

#############################
#   histogram utilities     #
#############################

def createBins(nbins,xmin,xmax):
    binwidth = (xmax-xmin)/float(nbins)
    bins = []
    for i in range(0,nbins+1):
        xb = xmin + float(i)*binwidth
        bins.append(xb)
    return bins

def zeroBinErrors(hist):
    nbins = hist.GetNbinsX()
    for i in range(1,nbins+1):
        hist.SetBinError(i,0.)

def createUnitHisto(hist,histName):
    nbins = hist.GetNbinsX()
    unitHist = hist.Clone(histName)
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        e = hist.GetBinError(i)
        if x>0:
            rat = e/x
            unitHist.SetBinContent(i,1.)
            unitHist.SetBinError(i,rat)

    return unitHist

def dividePassProbe(passHist,failHist,histName):
    nbins = passHist.GetNbinsX()
    hist = passHist.Clone(histName)
    for i in range(1,nbins+1):
        xpass = passHist.GetBinContent(i)
        epass = passHist.GetBinError(i)
        xfail = failHist.GetBinContent(i)
        efail = failHist.GetBinError(i)
        xprobe = xpass+xfail
        ratio = 1
        eratio = 0
        if xprobe>1e-4:
            ratio = xpass/xprobe
            dpass = xfail*epass/(xprobe*xprobe)
            dfail = xpass*efail/(xprobe*xprobe)
            eratio = math.sqrt(dpass*dpass+dfail*dfail)
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

def divideHistos(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        eDen = denHist.GetBinError(i)
        ratio = 1
        eratio = 0
        if xNum>1e-7 and xDen>1e-7:
            ratio = xNum/xDen
            rNum = eNum/xNum
            rDen = eDen/xDen
            rratio = math.sqrt(rNum*rNum+rDen*rDen)
            eratio = rratio * ratio
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

def histoRatio(numHist,denHist,histName):
    nbins = numHist.GetNbinsX()
    hist = numHist.Clone(histName)
    for i in range(1,nbins+1):
        xNum = numHist.GetBinContent(i)
        eNum = numHist.GetBinError(i)
        xDen = denHist.GetBinContent(i)
        ratio = 1
        eratio = 0
        if xNum>1e-7 and xDen>1e-7:
            ratio = xNum/xDen
            eratio = eNum/xDen
        hist.SetBinContent(i,ratio)
        hist.SetBinError(i,eratio)

    return hist

def interpolateHisto(x,hist):
    y,e = 1,0.1
    nbins = hist.GetNbinsX()
    if x<hist.GetBinCenter(1):
        return hist.GetBinContent(1),hist.GetBinError(1)
    if x>hist.GetBinCenter(nbins):
        return hist.GetBinContent(nbins),hist.GetBinError(nbins)
    for ib in range(1,nbins):
        x1 = hist.GetBinCenter(ib)
        x2 = hist.GetBinCenter(ib+1)
        if x>x1 and x<x2:
            y1 = hist.GetBinContent(ib)
            y2 = hist.GetBinContent(ib+1)
            e1 = hist.GetBinError(ib)
            e2 = hist.GetBinContent(ib+1)
            dx = x2 - x1
            dy = y2 - y1
            de = e2 - e1
            y = y1 + (x-x1)*dy/dx
            e = e1 + (x-x1)*de/dx
            return y,e
    return y,e

def rebinHisto(hist,bins,suffix):
    nbins = hist.GetNbinsX()
    newbins = len(bins)-1
    name = hist.GetName()+"_"+suffix
    newhist = ROOT.TH1D(name,"",newbins,array('d',list(bins)))
    for ib in range(1,nbins+1):
        centre = hist.GetBinCenter(ib)
        bin_id = newhist.FindBin(centre)
        xbin = hist.GetBinContent(ib)
        ebin = hist.GetBinError(ib)
        xnew = newhist.GetBinContent(bin_id)
        enew = newhist.GetBinError(bin_id)
        x_update = xbin + xnew;
        e_update = math.sqrt(ebin*ebin + enew*enew);
        newhist.SetBinContent(bin_id,x_update)
        newhist.SetBinError(bin_id,e_update)
    return newhist

##################################
# grouping background templates  #
##################################
def GroupBackgrounds(hists,groups):
    
    outhists = {}
    tot_first = True
    for group in groups:
        bkgs = groups[group]
        first = True
        for bkg in bkgs:
            if first:
                newhist = hists[bkg].Clone(group)
                outhists[group] = newhist
                first = False
            else:
                outhists[group].Add(outhists[group],hists[bkg],1.,1.)                

    first = True
    for group in groups:
        if first:
            newhist = outhists[group].Clone('tot_bkg')
            outhists['tot_bkg'] = newhist
            first = False
        else:
            outhists['tot_bkg'].Add(outhists['tot_bkg'],outhists[group],1.,1.)
    return outhists


##############################
#    Main plotting routine   #
##############################                
def Plot(hists,**kwargs):

    isBBA = False
    for hist in hists:
        if 'bbA' in hist:
            isBBA = True
    
    analysis = kwargs.get('analysis','azh')
    year = kwargs.get('year','2018')
    cat = kwargs.get('cat','0btag')
    channel = kwargs.get('channel','mmtt')
    mass = kwargs.get('mass','400')
    scale_bbA = kwargs.get('scale_bbA',1.)
    scale_ggA = kwargs.get('scale_ggA',1.)

    data_hist = hists['data'].Clone('data_hist')
    ggA_hist = hists['ggA'].Clone('ggA_hist')
    bbA_hist = ggA_hist
    if isBBA: bbA_hist = hists['bbA'].Clone('bbA_hist')
    
    fake_hist = hists['reducible_bkg']
    ZZ_hist = hists['ZZ_bkg']
    other_hist = hists['other_bkg']
    tot_hist = hists['tot_bkg']
    
    styles.InitData(data_hist)
    data_hist.SetLineColor(1)
    styles.InitHist(ZZ_hist,"","",ROOT.TColor.GetColor("#4496C8"),1001)
    styles.InitHist(fake_hist,"","",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(other_hist,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitModel(ggA_hist,ROOT.kRed)
    if isBBA: styles.InitModel(bbA_hist,ROOT.kBlue)
    styles.InitTotalHist(tot_hist)

    fake_hist.Add(fake_hist,other_hist)
    ZZ_hist.Add(ZZ_hist,fake_hist)

    zeroBinErrors(ZZ_hist)
    zeroBinErrors(fake_hist)
    zeroBinErrors(other_hist)
    zeroBinErrors(ggA_hist)
    zeroBinErrors(bbA_hist)

    ymax = 0
    nbins = data_hist.GetNbinsX()
    for ib in range(1,nbins+1):
        x = data_hist.GetBinContent(ib)
        err = data_hist.GetBinError(ib)
        xsum = x+err
        if xsum>ymax: ymax = xsum

    if tot_hist.GetMaximum()>ymax: 
        ymax = tot_hist.GetMaximum()

    data_hist.GetXaxis().SetLabelSize(0.05)
    data_hist.GetYaxis().SetLabelSize(0.05)
    data_hist.GetXaxis().SetTitleOffset(1.0)
    data_hist.GetYaxis().SetTitleOffset(1.2)
    data_hist.GetXaxis().SetTitleSize(0.06)
    data_hist.GetYaxis().SetTitleSize(0.06)
    
    data_hist.GetXaxis().SetTitle('m(4lepton) (GeV)')
    data_hist.GetYaxis().SetTitle('Events / bin')

    canv = styles.MakeCanvas('canv','',600,600) 
    data_hist.Draw('e1')
    ZZ_hist.Draw('hsame')
    fake_hist.Draw('hsame')
    other_hist.Draw('hsame')
    tot_hist.Draw('e2same')
    data_hist.Draw('e1same')

    leg = ROOT.TLegend(0.65,0.45,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(styles.fullchan_map[channel])
    leg.AddEntry(data_hist,'data','lp')
    leg.AddEntry(ZZ_hist,'ZZ','f')
    leg.AddEntry(fake_hist,'reducible','f')
    leg.AddEntry(other_hist,'other','f')
    leg.AddEntry(ggA_hist,'ggA'+mass,'l')
    if isBBA: leg.AddEntry(ggA_hist,'bbA'+mass,'l')
    leg.Draw()
    styles.CMS_label(canv,era=year,extraText='Internal')
    canv.SetLogx(True)
    canv.Update()
    canv.Print('figures/m4l_%s_%s_%s_%s_%s.png'%(analysis,year,cat,channel,mass))

