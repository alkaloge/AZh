
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

bins_fakes = [200,300,400,2400]

##############################
# AZh analysis : definitions # 
##############################

azh_masses = ['225','250','275','300','325','350','375','400','450','500','600','700','800','900','1000','1200','1400','1600','1800','2000']

azh_masses_ext = ['225','250','275','300','325','350','375','400','450','500','600','700','800','900','1000','1200','1400','1600','1800','2000','all']

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

azh_allbkgs = [
    "ggZHWW",
    "ZHWW",
    "TTHtt",
    "VVV",
    "TTZ",
    "ZHtt",
    "ggZZ",
    "ZZ",
    "ggHtt",  # -> cannot produce 4 genuine charged leptons
    "VBFHtt", # -> cannot produce 4 genuine charged leptons
    "WHtt",   # -> cannot produce 4 genuine charged leptons
    "ggHWW",  # -> cannot produce 4 genuine charged leptons
    "ggHZZ",  # -> negligible
    "VBFHWW", # -> cannot produce 4 genuine charged leptons
    "TTW",    # -> cannot produce 4 genuine charged leptons
    "TT",     # -> cannot produce 4 genuine charged leptons
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

azh_channels_noem = [
    'eeet',
    'eemt',
    'eett',
    'mmet',
    'mmmt',
    'mmtt',
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
    'JES',
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
    nameCentral = hist.GetName()
    nameUp = histUp.GetName()
    nameDown = histDown.GetName()
    if nbins!=nbinsUp or nbins!=nbinsDown:
        print('symmetrizeUnc : inconsistency between number of bins (central/up/down) %s %s %s'%(nameCentral,nameUp,nameDown))


    for ib in range(1,nbins+1):
        xcentral = hist.GetBinContent(ib)
        xup = histUp.GetBinContent(ib)
        xdown = histDown.GetBinContent(ib)
        delta = 0.5*(xup-xdown)
        up = max(0,xcentral+delta)
        down = max(0,xcentral-delta)
        # symmetrize shape templates
        #        onesided = (xcentral<xdown and xcentral<xup) or (xcentral>xdown and xcentral>xup)
        #        if onesided:

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
        print('addHistos: inconsistency of bins: %2i and %2i in %s and %s '%(nbins1,nbins2,hist1.GetName(),hist2.GetName()))
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
    
    styles.InitData(hist,"m_{ll#tau#tau}^{cons} [GeV]","dN/dm [1/GeV]")
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

    if sys.lower()!='none':
        histRatioUp = histUp.Clone('histRatioUp')
        histRatioDown = histDown.Clone('histRatioDown')

    histRatio = hist.Clone('histRatio') 
    maxdiff = 0
    for ib in range(nbins+1):
        value = hist.GetBinContent(ib)
        error = hist.GetBinError(ib)
        ratio = 1
        eratio = 0.
        if value>0: 
            eratio = error/value
            if sys.lower()!='none':
                value_up = histUp.GetBinContent(ib)
                value_down = histDown.GetBinContent(ib)
                histRatioUp.SetBinContent(ib,value_up/value)
                histRatioDown.SetBinContent(ib,value_down/value)
                
        histRatio.SetBinError(ib,eratio)
        histRatio.SetBinContent(ib,1.0)
    
    histRatio.GetYaxis().SetRangeUser(0.8,1.2)

    canv_name = 'canv_%s_%s'%(templ,sys)
    canv = styles.MakeCanvas(canv_name,'',700,700)
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)

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

    styles.CMS_label(upper,era=year,extraText='Simulation')

    upper.Update()
    upper.SetLogx(logx)
    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()

    canv.cd()

    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)
    
    histRatio.Draw('e1')
    histRatioUp.Draw('hsame')
    histRatioDown.Draw('hsame')

    styles.InitRatioHist(histRatio)

    lower.Modified()
    lower.RedrawAxis()
    lower.SetLogx(logx)
    
    # update canvas 
    canv.cd()
    canv.Modified()
    canv.cd()
    canv.SetSelected(canv)
    canv.Update()

    if sys.lower()=='none':
        canv.Print("%s/%s_%s_%s_%s_%s.png"%(FiguresFolder,analysis,year,cat,channel,templ))
    else:
        canv.Print("%s/%s_%s_%s_%s_%s_%s.png"%(FiguresFolder,analysis,year,cat,channel,templ,sys))

    print

###############################################
# plotting final discriminant from datacards 
                
def Plot(hists,fractions,**kwargs):

    isBBA = False
    for hist in hists:
        if 'bbA' in hist:
            isBBA = True
    
    year = kwargs.get('year','2018')
    cat = kwargs.get('cat','0btag')
    channel = kwargs.get('channel','mmtt')
    mass = kwargs.get('mass','300')
    scale_bbA = kwargs.get('scale_bbA',5.)
    scale_ggA = kwargs.get('scale_ggA',5.)
    xmin = kwargs.get('xmin',199.9)
    xmax = kwargs.get('xmax',1150.1)
    ratiomin = kwargs.get('ratiomin',0.)
    ratiomax = kwargs.get('ratiomax',2.2)
    blind = kwargs.get('blind',True)
    logx = kwargs.get('logx',True)
    logy = kwargs.get('logy',False)
    fittype = kwargs.get('fittype','prefit')
    postfix = kwargs.get('postfix','cards')
    plotSignal = kwargs.get('plotSignal',False)
    show_yield = kwargs.get('show_yield',False)

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
    styles.InitHist(ZZ_hist,"","",ROOT.TColor.GetColor("#4496C8"),1001)
    styles.InitHist(fake_hist,"","",ROOT.TColor.GetColor("#c6f74a"),1001)
    styles.InitHist(other_hist,"","",ROOT.TColor.GetColor("#FFCCFF"),1001)

    styles.InitHist(ZZ_hist,"","",ROOT.TColor.GetColor("#ffa90e"),1001) #red
    styles.InitHist(fake_hist,"","",ROOT.TColor.GetColor("#e76300"),1001)
    styles.InitHist(other_hist,"","",ROOT.TColor.GetColor("#3f90da"),1001)
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

    # prefit and postfit correlated constraints 
    # xsecs for ZZ, ttZ, VV and Higgs bkg
    # and reducible systematics
    other_sys = 0.25
    ZZ_sys = 0.05
    fake_total = fractions['et'] + fractions['mt'] + fractions['tt']
    fake_sys = (0.2*fractions['et']+0.15*fractions['mt']+0.15*fractions['tt'])/fake_total
    if fittype=='fit_b' or fittype=='fit_s':
        fake_sys = (0.15*fractions['et']+0.1*fractions['mt']+0.1*fractions['tt'])/fake_total
        ZZ_sys = 0.03
        other_sys = 0.21

    ymin = 0.
    ymax = 0.
    nbins = data_hist.GetNbinsX()
    xdata = []
    exdata = []
    ydata = []
    eyldata = []
    eyhdata = []
    ydata_ratio = []
    eyldata_ratio = []
    eyhdata_ratio = []
    for ib in range(1,nbins+1):
        x = data_hist.GetBinContent(ib)
        err = data_hist.GetBinError(ib)
        xcenter = data_hist.GetBinCenter(ib)
        binwidth = data_hist.GetBinWidth(ib)
        binratio = 1.0/binwidth
        if show_yield:
            binratio = 1.0
        err_ZZ = ZZ_hist.GetBinContent(ib)*ZZ_sys
        err_other = other_hist.GetBinContent(ib)*other_sys
        err_fake = fake_hist.GetBinContent(ib)*fake_sys
        err_tot = tot_hist.GetBinError(ib)
        err_tot = math.sqrt(err_tot*err_tot+err_ZZ*err_ZZ+err_fake*err_fake+err_other*err_other)
        tot_hist.SetBinError(ib,err_tot)
        ZZ_hist.SetBinContent(ib,binratio*ZZ_hist.GetBinContent(ib))
        ZZ_hist.SetBinError(ib,binratio*ZZ_hist.GetBinError(ib))
        fake_hist.SetBinContent(ib,binratio*fake_hist.GetBinContent(ib))
        fake_hist.SetBinError(ib,binratio*fake_hist.GetBinError(ib))
        other_hist.SetBinContent(ib,binratio*other_hist.GetBinContent(ib))
        other_hist.SetBinError(ib,binratio*other_hist.GetBinError(ib))
        tot_hist.SetBinContent(ib,binratio*tot_hist.GetBinContent(ib))
        tot_hist.SetBinError(ib,binratio*tot_hist.GetBinError(ib))
        ggA_hist.SetBinContent(ib,binratio*ggA_hist.GetBinContent(ib))
        if isBBA: bbA_hist.SetBinContent(ib,binratio*bbA_hist.GetBinContent(ib))
        
        # filling vectors for data graph and data/MC ratio graph
        xdata.append(xcenter)
        exdata.append(0.0)
        y_obs = x*binratio
        if logy and x==0:
            y_obs = 1e-8
        ydata.append(y_obs)
        eyldata.append(binratio*(-0.5+math.sqrt(x+0.25)))
        eyhdata.append(binratio*(0.5+math.sqrt(x+0.25)))
        ydata_ratio.append(y_obs/tot_hist.GetBinContent(ib))
        eyldata_ratio.append(binratio*(-0.5+math.sqrt(x+0.25))/tot_hist.GetBinContent(ib))
        eyhdata_ratio.append(binratio*(0.5+math.sqrt(x+0.25))/tot_hist.GetBinContent(ib))
        xsum = (x+err)*binratio
        if xsum>ymax: ymax = xsum

    data_graph = ROOT.TGraphAsymmErrors(nbins,
                                        array('d',list(xdata)),
                                        array('d',list(ydata)),
                                        array('d',list(exdata)),
                                        array('d',list(exdata)),
                                        array('d',list(eyldata)),
                                        array('d',list(eyhdata)))

    data_graph_ratio = ROOT.TGraphAsymmErrors(nbins,
                                              array('d',list(xdata)),
                                              array('d',list(ydata_ratio)),
                                              array('d',list(exdata)),
                                              array('d',list(exdata)),
                                              array('d',list(eyldata_ratio)),
                                              array('d',list(eyhdata_ratio)))

    data_graph.SetMarkerStyle(20)
    data_graph.SetMarkerSize(1.5)
    data_graph.SetMarkerColor(1)

    data_graph_ratio.SetMarkerStyle(20)
    data_graph_ratio.SetMarkerSize(1.5)
    data_graph_ratio.SetMarkerColor(1)

    unit_ratio = createUnitHisto(tot_hist,'unit_ratio')
    unit_ratio.GetYaxis().SetRangeUser(ratiomin,ratiomax)
    unit_ratio.GetXaxis().SetRangeUser(xmin,xmax)

    ggA_unit = ggA_hist.Clone('ggA_unit')

    if fittype=='fit_s':
        for ib in range(1,nbins+1):
            sig_ggA = ggA_hist.GetBinContent(ib)
            sig_bbA = bbA_hist.GetBinContent(ib)
            bkg = tot_hist.GetBinContent(ib)
            total = sig_ggA + sig_bbA + bkg
            ratio_sig = total/bkg
            ggA_hist.SetBinContent(ib,total)
            ggA_unit.SetBinContent(ib,ratio_sig)

    if blind: 
        ymax = tot_hist.GetMaximum()

    if tot_hist.GetMaximum()>ymax: 
        ymax = tot_hist.GetMaximum()
    if ggA_hist.GetMaximum()>ymax:
        ymax = ggA_hist.GetMaximum()
    if isBBA:
        if bbA_hist.GetMaximum()>ymax:
            ymax = bbA_hist.GetMaximum()

    if logy:
        ymin = 1e-3
        ymax *= 50.
    else:
        ymin = 0.
        ymax *= 1.1


    frame = ROOT.TH2D('frame','',2,xmin,xmax,2,ymin,ymax)
    styles.InitTotalHist(frame)
    frame.GetYaxis().SetTitle("dN/dm (1/GeV)")
    if show_yield:
        frame.GetYaxis().SetTitle("Events / bin")
    frame.GetYaxis().SetTitleOffset(1.2)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetLabelSize(0.055)
    frame.GetXaxis().SetLabelSize(0)

    frameRatio = ROOT.TH2D('frameRatio','',2,xmin,xmax,2,ratiomin,ratiomax)
    styles.InitTotalHist(frameRatio)
    styles.InitRatioHist(frameRatio)
    frameRatio.GetYaxis().SetTitle("obs/bkg")
    frameRatio.GetXaxis().SetTitle("m_{ll#tau#tau}^{cons} (GeV)")

    if logx:
        frame.GetXaxis().SetNdivisions(505)
        frame.GetXaxis().SetMoreLogLabels()
        frame.GetXaxis().SetNoExponent()
        frameRatio.GetXaxis().SetNdivisions(505)
        frameRatio.GetXaxis().SetMoreLogLabels()
        frameRatio.GetXaxis().SetNoExponent()

    canv = styles.MakeCanvas('canv','',600,700) 

    # upper pad
    upper = ROOT.TPad("upper", "pad",0,0.31,1,1)
    upper.Draw()
    upper.cd()
    styles.InitUpperPad(upper)
    
    frame.Draw('h')
    ZZ_hist.Draw('hsame')
    fake_hist.Draw('hsame')
    other_hist.Draw('hsame')
    tot_hist.Draw('e2same')
    if not blind: 
        data_graph.Draw('pe1same')
    if plotSignal:
        if fittype=='fit_s':
            ggA_hist.Draw('hsame')
        else:
            ggA_hist.Draw('hsame')
            if isBBA: bbA_hist.Draw('hsame')
    if not blind:
        data_graph.Draw('pe1same')

    legTitle = cat;
    if channel in ['et','mt','tt']:
        legTitle + styles.fullchan_map[channel]

    leg = ROOT.TLegend(0.7,0.40,0.9,0.70)
    styles.SetLegendStyle(leg)
    leg.SetTextSize(0.045)
    leg.SetHeader(legTitle)
    if not blind: leg.AddEntry(data_hist,'data','lp')
    leg.AddEntry(ZZ_hist,'ZZ','f')
    leg.AddEntry(fake_hist,'reducible','f')
    leg.AddEntry(other_hist,'other','f')
    if plotSignal:
        if fittype=='fit_s':
            leg.AddEntry(ggA_hist,'A('+mass+')','l')
        else:
            leg.AddEntry(ggA_hist,'ggA'+mass+' (5 fb)','l')
            if isBBA: leg.AddEntry(bbA_hist,'bbA'+mass+ ' (5 fb)','l')
    leg.Draw()
    styles.CMS_label(upper,era=year,extraText='Preliminary')

    upper.SetLogx(logx)
    upper.SetLogy(logy)
    upper.Draw("SAME")
    upper.RedrawAxis()
    upper.Modified()
    upper.Update()
    canv.cd()
    canv.Update()

    # lower pad
    lower = ROOT.TPad("lower", "pad",0,0,1,0.30)
    lower.Draw()
    lower.cd()
    styles.InitLowerPad(lower)

    frameRatio.Draw('h')
    if fittype=='fit_s' and plotSignal: 
        ggA_unit.Draw('hsame')
    line = ROOT.TLine(xmin,1.,xmax,1.)
    line.SetLineColor(4)
    line.Draw()

    unit_ratio.Draw('e2same')
    data_graph_ratio.Draw('pe1same')

    lower.Modified()
    lower.RedrawAxis()
    lower.SetLogx(logx)
    lower.SetGridx(True)
    canv.cd()
    canv.Modified()
    canv.SetSelected(canv)
    canv.Update()

    if logy:
        postfix += '_logy'
    if cat=='':
        if channel=='':
            canv.Print('%s/m4l_%s_%s_%s.png'%(FiguresFolder,year,mass,postfix))
        else:
            canv.Print('%s/m4l_%s_%s_%s_%s.png'%(FiguresFolder,year,channel,mass,postfix))
    else:
        if channel=='':
            canv.Print('%s/m4l_%s_%s_%s_%s.png'%(FiguresFolder,year,cat,mass,postfix))
        else:
            canv.Print('%s/m4l_%s_%s_%s_%s_%s.png'%(FiguresFolder,year,cat,channel,mass,postfix))

###############################################

def GetInputFiles(**kwargs):

    year=kwargs.get('year','2018')
    cat=kwargs.get('cat','0btag')
    channel=kwargs.get('channel')
    mass=kwargs.get('mass','400')
    folder = kwargs.get('folder','datacards')

    path = BaseFolder+'/'+folder+'/Run2/'+mass
    filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
    filename_signal = filename

    fullfilename = path+'/'+filename
    fullfilename_signal = path+'/'+filename_signal
    if not os.path.isfile(fullfilename):
        print('file %s not found'%(fullfilename))
        exit()
    inputfile = ROOT.TFile(fullfilename)
    if inputfile==None:
        print('file %s not found'%(fullfilename))
        exit()
    if not os.path.isfile(fullfilename_signal):
        print('file %s not found'%(fullfilename))
        exit()
    inputfile_signal = ROOT.TFile(fullfilename_signal)
    if inputfile_signal==None:
        print('file %s not found'%(fullfilename_signal))
        exit()

    print
    print('Extracting histograms for year=%s  channel=%s  category=%s'%(year,cat,channel))
    print('from file %s'%(fullfilename))
    print

    return inputfile,inputfile_signal

