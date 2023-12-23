
import ROOT 
import math
from array import array
import numpy as np
import os
import AZh.combine.stylesAZh as styles

#############################
##### working dir ###########
#############################
BaseFolder=os.getenv('CMSSW_BASE')+'/src/AZh/combine'

#######################
# folder  for figures #
#######################
FiguresFolder = BaseFolder+'/figures'
DatacardsFolder = BaseFolder+'/datacards'
JobFolder = BaseFolder+'/jobs'

###################
#  luminosities   #
###################

eraLumi = {
    "2016" : 36300,
    "2016_postVFP" : 16800,
    "2016_preVFP"  : 19500,
    "2017" : 41480,    
    "2018" : 59830
}

#############################

years = ['2016','2017','2018']
years_ext = ['2016','2017','2018','Run2']

variations = ["Up","Down"]

bins_fakes = [200,400,700,2000]

##############################
# AZh analysis : definitions # 
##############################

azh_masses = ['225','275','300','325','350','375','400','450','500','600','700','800','900','1000','1200','1400','1600','1800','2000']

azh_masses_ext = ['225','275','300','325','350','375','400','450','500','600','700','800','900','1000','1200','1400','1600','1800','2000','all']

azh_bkgs = [
    "ggZHWW",
    "ZHWW",
    "TTHtt",
    "VVV",
    "TTZ",
    "ZHtt",
    "ggZZ",
    "ZZ",    
    "reducible"
]

azh_groupbkgs = {
    'reducible_bkg' : ['reducible'],
    'ZZ_bkg' : ['ZZ','ggZZ'],
    'other_bkg' : ['TTZ','VVV','ZHtt','TTHtt','ZHWW','ggZHWW']
}

azh_btagmap = {
    '0btag': '0',
    'btag': '1'
}

azh_signals = [
    'ggA',
    'bbA'
]

azh_cats = ['btag', '0btag']

azh_cats_ext = ['btag', '0btag', 'all']

azh_higgs_channels = {
    'eeem' : 'em',
    'eeet' : 'et',
    'eemt' : 'mt',
    'eett' : 'tt',
    'mmem' : 'em',
    'mmet' : 'et',
    'mmmt' : 'mt',
    'mmtt' : 'tt'
}

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

azh_channels_ext = [
    'eeem',
    'eeet',
    'eemt',
    'eett',
    'mmem',
    'mmet',
    'mmmt',
    'mmtt',
    'all'
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

azh_fakeuncs = [
    'bin1',
    'bin2',
    'bin3'
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

hig18023_cats = [
    "0btag"
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

hig18023_uncs = [
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

##################################
# Symmetrizing up/down templates #
##################################
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
        xcentral = hist.GetBinContent(ib)
        xup = histUp.GetBinContent(ib)
        xdown = histDown.GetBinContent(ib)
        delta = 0.5*(xup-xdown)
        up = max(0,xcentral+delta)
        down = max(0,xcentral-delta)
        onesided = (xcentral<xdown and xcentral<xup) or (xcentral>xdown and xcentral>xup)
        if onesided:
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

def fixNegativeBins(hist):
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        x = hist.GetBinContent(ib)
        e = hist.GetBinError(ib)
        if x<e:
            hist.SetBinContent(ib,0.5*e)
            hist.SetBinError(ib,0.5*e)


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

def addHistos(hist1,hist2):
    nbins1 = hist1.GetNbinsX()
    nbins2 = hist2.GetNbinsX()
    if nbins1!=nbins2:
        print
        print('addHistos: inconsistency of bins: %2i and %2i',nbins1,nbins2)
    else:
        for ib in range(1,nbins1+1):
            x1 = hist1.GetBinContent(ib)
            e1 = hist1.GetBinError(ib)
            x2 = hist2.GetBinContent(ib)
            e2 = hist2.GetBinError(ib)
            x = x1 + x2
            e = math.sqrt(e1*e1+e2*e2)
            hist1.SetBinContent(ib,x)
            hist1.SetBinError(ib,e)


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

def getNormError(hist):
    nbins = hist.GetNbinsX()
    norm = 0
    err2 = 0
    for ib in range(1,nbins+1):
        norm += hist.GetBinContent(ib)
        e = hist.GetBinError(ib)
        err2 += e*e
    err=math.sqrt(err2)
    return norm,err


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


##################################
# Plotting individual templates  #
##################################
def PlotTemplate(hists,**kwargs):

    hist = hists['central']
    histUp = hists['up']
    histDown = hists['down']

    analysis = kwargs.get('analysis','azh')

    year = kwargs.get('year','2016')
    cat = kwargs.get('cat','0btag')
    channel = kwargs.get('channel','mmtt')

    templ = kwargs.get('templ','data_obs')
    sys = kwargs.get('sys','')

    prnt = kwargs.get('verbosity',True)
    xmin = kwargs.get('xmin',201.0)
    xmax = kwargs.get('xmax',699.0)
    logx = kwargs.get('logx',False)

    nbins = hist.GetNbinsX()
    if prnt:
        print
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print
        if sys.lower()=='none':
            print('plotting template : era=%s  category=%s  channel=%s  proc=%s'%(year,cat,channel,templ))
        else:
            print('plotting template : era=%s  category=%s  channel=%s  proc=%s  sys=%s'%(year,cat,channel,templ,sys))
        print
        
        if sys.lower()=='none':
            print('  mass bin   value +/- stat. unc')
        else:
            print('  mass bin    central      up      down')
                
        print('-----------------------------------------')
    
    norm = 0
    ymax = 0
    for i in range(1,nbins+1):
        x = hist.GetBinContent(i)
        ex = hist.GetBinError(i)
        ilow = int(hist.GetBinLowEdge(i))
        ihigh = int(hist.GetBinLowEdge(i+1))
        current = x+ex
        if current>ymax: ymax = current
        if prnt:
            if sys.lower()=='none':
                print('[%4i,%4i]   %5.3f +/- %5.3f'%(ilow,ihigh,x,ex))
            else:
                xup = histUp.GetBinContent(i)
                xdown = histDown.GetBinContent(i)
                print('[%4i,%4i]   %7.5f   %7.5f   %7.5f'%(ilow,ihigh,x,xup,xdown))            

    if prnt:
        Yield=hist.GetSumOfWeights()
        print
        if sys.lower()=='none':
            print('Overall yield = %7.4f'%(Yield))
        else:
            YieldUp=histUp.GetSumOfWeights()
            YieldDown=histDown.GetSumOfWeights()
            print('Overall yield : central = %7.4f, up = %7.4f, down = %7.4f'
                  %(Yield,YieldUp,YieldDown))
        print
    
    styles.InitData(hist,"m(4l) [GeV]","Events")
    hist.GetXaxis().SetNdivisions(505)
    if sys.lower()!='none':
        styles.InitModel(histUp,ROOT.kRed,1)
        styles.InitModel(histDown,ROOT.kBlue,1)

        styles.zeroBinErrors(histUp)
        styles.zeroBinErrors(histDown)

    ymax = 0 
    nbins = hist.GetNbinsX()
    for ib in range(1,nbins+1):
        x = hist.GetBinContent(ib)
        e = hist.GetBinError(ib)
        y = x+e
        if y>ymax: ymax=y

    if sys.lower()!='none':
        if histUp.GetMaximum()>ymax: ymax = histUp.GetMaximum()
        if histDown.GetMaximum()>ymax: ymax = histDown.GetMaximum()

    hist.GetYaxis().SetRangeUser(0.,1.1*ymax)
    hist.GetXaxis().SetRangeUser(xmin,xmax)
    
    canv_name = 'canv_%s_%s'%(templ,sys)
    canv = styles.MakeCanvas(canv_name,'',700,700)
    hist.Draw("e1")
    if sys.lower()!='none':
        histUp.Draw("hsame")
        histDown.Draw("hsame")

    leg = ROOT.TLegend(0.63,0.45,0.9,0.70)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.033)
    leg.SetHeader(year+" "+cat+"_"+channel)
    leg.AddEntry(hist,templ,'lp')
    if sys.lower()!='none':
        leg.AddEntry(histUp,sys+'Up','l')
        leg.AddEntry(histDown,sys+'Down','l')
    leg.Draw()

    styles.CMS_label(canv,era=year,extraText='Simulation')

    canv.SetLogx(logx)
    canv.Update()
    if sys.lower()=='none':
        canv.Print("%s/%s_%s_%s_%s_%s.png"%(FiguresFolder,analysis,year,cat,channel,templ))
    else:
        canv.Print("%s/%s_%s_%s_%s_%s_%s.png"%(FiguresFolder,analysis,year,cat,channel,templ,sys))

    print

###############################################
# plotting final discriminant from datacards 
                
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
    scale_bbA = kwargs.get('scale_bbA',5.)
    scale_ggA = kwargs.get('scale_ggA',5.)
    xmin = kwargs.get('xmin',200)
    xmax = kwargs.get('xmax',700)
    blind = kwargs.get('blind',True)
    logx = kwargs.get('logx',True)

    data_hist = hists['data'].Clone('data_hist')
    ggA_hist = hists['ggA'].Clone('ggA_hist')
    bbA_hist = ggA_hist
    if isBBA: bbA_hist = hists['bbA'].Clone('bbA_hist')

    ggA_hist.Scale(scale_ggA)
    if isBBA: bbA_hist.Scale(scale_bbA)
    
    fake_hist = hists['reducible_bkg']
    ZZ_hist = hists['ZZ_bkg']
    other_hist = hists['other_bkg']
    tot_hist = hists['tot_bkg']
    
    styles.InitData(data_hist,"","")    
    styles.InitHist(ZZ_hist,"m(4l) [GeV]","Events",ROOT.TColor.GetColor("#4496C8"),1001)
    styles.InitHist(fake_hist,"","",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(other_hist,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)
    styles.InitModel(ggA_hist,ROOT.kRed,1)
    if isBBA: styles.InitModel(bbA_hist,ROOT.kBlue,2)
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

    ZZ_hist.GetXaxis().SetRangeUser(xmin,xmax)
    ZZ_hist.GetYaxis().SetRangeUser(0,1.2*ymax)

    if logx:
        ZZ_hist.GetXaxis().SetNdivisions(505)
        ZZ_hist.GetXaxis().SetMoreLogLabels()
        ZZ_hist.GetXaxis().SetNoExponent()
        ZZ_hist.GetXaxis().SetMoreLogLabels()
    
    canv = styles.MakeCanvas('canv','',600,600) 
    ZZ_hist.Draw('h')
    fake_hist.Draw('hsame')
    other_hist.Draw('hsame')
    tot_hist.Draw('e2same')
    if not blind: data_hist.Draw('e1same')
    ggA_hist.Draw('hsame')
    if isBBA: bbA_hist.Draw('hsame')

    legTitle = cat;
    if channel!='':
        legTitle + styles.fullchan_map[channel]

    leg = ROOT.TLegend(0.6,0.45,0.9,0.7)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.04)
    leg.SetHeader(legTitle)
    if not blind: leg.AddEntry(data_hist,'data','lp')
    leg.AddEntry(ZZ_hist,'ZZ','f')
    leg.AddEntry(fake_hist,'reducible','f')
    leg.AddEntry(other_hist,'other','f')
    leg.AddEntry(ggA_hist,'ggA'+mass+' (20 fb)','l')
    if isBBA: leg.AddEntry(bbA_hist,'bbA'+mass+ '(20 fb)','l')
    leg.Draw()
    styles.CMS_label(canv,era=year,extraText='Internal')
    canv.SetLogx(logx)
    canv.RedrawAxis()
    canv.Update()
    if cat=='':
        if channel=='':
            canv.Print('%s/m4l_%s_%s_%s.png'%(FiguresFolder,analysis,year,mass))
        else:
            canv.Print('%s/m4l_%s_%s_%s_%s.png'%(FiguresFolder,analysis,year,channel,mass))
    else:
        if channel=='':
            canv.Print('%s/m4l_%s_%s_%s_%s.png'%(FiguresFolder,analysis,year,cat,mass))
        else:
            canv.Print('%s/m4l_%s_%s_%s_%s_%s.png'%(FiguresFolder,analysis,year,cat,channel,mass))

###############################################

def GetInputFiles(**kwargs):

    analysis=kwargs.get('analysis','azh')
    year=kwargs.get('year','2018')
    cat=kwargs.get('cat','0btag')
    channel=kwargs.get('channel')
    mass=kwargs.get('mass','400')

    folder = BaseFolder+'/root_files'
    filename = 'MC_data_'+cat+'_'+year+'.root'
    filename_signal = 'signal_'+mass+'_'+cat+'_'+year+'.root'

    if analysis.lower()=='azh':
        folder = BaseFolder+'/datacards/Run2/'+mass
        filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
        filename_signal = filename
    elif analysis.lower()=='hig18023':
        folder = BaseFolder+'/HIG-18-023/datacards/'+hig18023_channels[channel]+'/Aconstr_HsvFit90/common'
        filename = 'SR.input.root'
        filename_signal = filename

    fullfilename = folder+'/'+filename
    fullfilename_signal = folder+'/'+filename_signal
    inputfile = ROOT.TFile(fullfilename)
    if inputfile==None:
        print('file %s not found'%(fullfilename))
        exit(1)
    inputfile_signal = ROOT.TFile(fullfilename_signal)
    if inputfile_signal==None:
        print('file %s not found'%(fullfilename_signal))
        exit(1)

    print
    print('Extracting histograms for year=%s  channel=%s  category=%s'%(year,cat,channel))
    print('form file %s'%(fullfilename))
    print

    return inputfile,inputfile_signal

