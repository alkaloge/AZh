#!/usr/bin/env python

import ROOT
import os
import AZh.combine.utilsAZh as utils

########################################################################
# new tau ID scale factors for UL2016 are 6% higher than previous ones #
# updated scale factors have been released in summer 2023              #
# https://indico.cern.ch/event/1264653                                 #
# https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2  #
########################################################################
tauID_UL2016 = {
    'eeem' : 1.00,
    'eeet' : 1.06,
    'eemt' : 1.06,
    'eett' : 1.12,
    'mmem' : 1.00,
    'mmet' : 1.06,
    'mmmt' : 1.06,
    'mmtt' : 1.12
}

uncertainties = [
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
    'eleSmear',
    'JES',
    'JER'
]

def RebinAndSave(**kwargs):

    era = kwargs.get('year','2018')
    binning = kwargs.get('binning','nominal')
    years = []
    if era=='Run2':
        years = utils.years
    else:
        years.append(era)

    subfolder = kwargs.get('folder','coffea')
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_allbkgs
    uncs = uncertainties
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    variations = utils.variations
    signals = utils.azh_signals

    path = folder+'/'+subfolder
    if os.path.isdir(path):
        print('')
        print('Processing files in folder ->')
        print('%s'%(path))
        #        os.system('rm root_files/*.root')
        print('')
    else:
        print('')
        print('Folder %s does not exist'%(path))
        exit()

    ###########################
    # defininting of binning
    ###########################
    bins_ggA = []
    bins_bbA = []
    if binning=='nominal':
        for ib in range(200,500,20):
            bins_ggA.append(ib)    
        for ib in range(500,750,25):
            bins_ggA.append(ib)
        for ib in range(750,1150,100):
            bins_ggA.append(ib)
        bins_ggA.append(2400)
        bins_bbA=bins_ggA            
    elif binning=='fine':
        for ib in range(200,500,10):
            bins_ggA.append(ib)    
        for ib in range(500,750,25):
            bins_ggA.append(ib)
        for ib in range(750,1150,100):
            bins_ggA.append(ib)
        bins_ggA.append(2400)
        bins_bbA=bins_ggA
    else:
        for ib in range(200,400,20):
            bins_ggA.append(ib)
        bins_ggA.append(400)
        bins_ggA.append(450)
        bins_ggA.append(550)
        bins_ggA.append(700)
        bins_ggA.append(1000)
        bins_ggA.append(2400)
        bins_bbA=bins_ggA

    bins_cat = {
        'btag': bins_bbA,
        '0btag': bins_ggA
    }

    print('')
    print('Rebinning 0btag with bins ->')
    nbins = len(bins_ggA)
    for ib in range(0,nbins-1):
        print('[%4i,%4i]'%(int(bins_ggA[ib]),int(bins_ggA[ib+1])))
    print('')
    print('Rebinning btag with bins ->')
    nbins = len(bins_bbA)
    for ib in range(0,nbins-1):
        print('[%4i,%4i]'%(int(bins_bbA[ib]),int(bins_bbA[ib+1])))
    print('')

    for year in years:
        for cat in cats:
            bins = bins_cat[cat]
            print('Rebinning %s %s '%(year,cat))
            print(' background templates')
            name_data = folder+'/'+subfolder+'/data_'+cat+'_'+year+'.root'
            name_mc   = folder+'/'+subfolder+'/MC_'+cat+'_'+year+'.root'
            input_data = ROOT.TFile(name_data)
            input_mc = ROOT.TFile(name_mc)
            name_output = folder+'/MC_data_'+cat+'_'+year+'.root'
            output_file = ROOT.TFile(name_output,'recreate')
            for channel in channels:
                output_file.mkdir(channel)
                data_orig = input_data.Get(channel+'/data')
                data_rebin = utils.rebinHisto(data_orig,bins,'_rebin')
                output_file.cd(channel)
                data_rebin.Write('data')
                for template in templates:
                    mc_orig = input_mc.Get(channel+'/'+template)
                    if mc_orig!=None:
                        mc_rebin = utils.rebinHisto(mc_orig,bins,year+cat+'_rebin')
                        output_file.cd(channel)
                        mc_rebin.Write(template)
                    else:
                        print('Template %s is not found in channel %s and category %s'%(template,channel,cat))
                        
                    for unc in uncs:
                        for variation in variations:
                            sys_orig =  input_mc.Get(channel+'/'+template+'_'+unc+variation)
                            if sys_orig!=None:
                                sys_rebin = utils.rebinHisto(sys_orig,bins,year+cat+'_rebin')
                                output_file.cd(channel)
                                sys_rebin.Write(template+'_'+unc+variation)
            output_file.Close()
            for mass in masses:
                print(' signal with mass %s'%(mass))
                name_output = folder+'/signal_'+mass+'_'+cat+'_'+year+'.root'
                name_input = folder+'/'+subfolder+'/signal_'+mass+'_'+cat+'_'+year+'.root'
                input_file = ROOT.TFile(name_input)
                output_file = ROOT.TFile(name_output,'recreate')
                for channel in channels:
                    output_file.mkdir(channel)
                    for signal in signals:
                        sig_orig = input_file.Get(channel+'/'+signal)
                        sig_rebin = utils.rebinHisto(sig_orig,bins,year+cat+'_rebin')
                        output_file.cd(channel)
                        sig_rebin.Write(signal)
                        for unc in uncs:
                            for variation in variations:
                                sys_orig = input_file.Get(channel+'/'+signal+'_'+unc+variation)
                                sys_rebin = utils.rebinHisto(sys_orig,bins,year+cat+'_rebin')
                                output_file.cd(channel)
                                sys_rebin.Write(signal+'_'+unc+variation)
                output_file.Close()
    for h_channel in ['em','et','mt','tt']:
        command = 'cp root_files/%s/%s*root root_files/'%(subfolder,h_channel)
        os.system(command)


def MergeDataMC(**kwargs):

    folder = kwargs.get('folder','tighten_mtt')
    era = kwargs.get('year','2018')
    years = []
    if era=='Run2':
        years = utils.years
    else:
        years.append(era)
    
    #    os.system('rm root_files/*.root')
    pathdir='root_files/%s'%(folder)
    if os.path.isdir(pathdir):
        command='cp root_files/%s/*root root_files'%(folder)
        os.system(command)
    else:
        print('folder root_files/%s does not exist'%(folder))
        exit()
    for year in years:
        command='./Hadd_MC_data.bash %s'%(year)
        os.system(command)

def FixNegativeBins(**kwargs):

    era = kwargs.get('year','2018')
    years = []
    if era=='Run2':
        years = utils.years
    else:
        years.append(era) 
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_allbkgs
    uncs = uncertainties
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    variations = utils.variations
    for year in years:
        for cat in cats:
            nameinput = folder + "/MC_data_"+cat+"_"+year+".root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
            
                hist = inputfile.Get(channel+'/data')
                histToWrite = hist.Clone(channel+'data_obs')
                inputfile.cd(channel)
                histToWrite.Write('data_obs')
                for template in templates:
                    hist = inputfile.Get(channel+'/'+template)
                    nbins = hist.GetNbinsX()
                    for ib in range(1,nbins+1):
                        x = hist.GetBinContent(ib)
                        if x<1e-6:
                            if x<0: 
                                print('negative bin %2i :  %7.5f in %s_%s_%s %s'%(ib,x,year,cat,channel,template))
                            hist.SetBinContent(ib,1e-6)
                            hist.SetBinError(ib,0.3e-6)
                    inputfile.cd(channel)
                    if hist.GetSumOfWeights()==0.0:
                        hist.SetBinContent(1,0.001)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                for ib in range(1,nbins+1):
                                    x = histSys.GetBinContent(ib)
                                    if x<1e-6:
                                        if x<0: 
                                            print('negative bin %2i : %7.5f in %s_%s_%s %s_%s%s'%(ib,x,year,cat,channel,template,unc,variation))
                                        histSys.SetBinContent(ib,1e-6)
                                        histSys.SetBinError(ib,0.3e-6)
                                inputfile.cd(channel)
                                if histSys.GetSumOfWeights()==0.0:
                                    histSys.SetBinContent(1,0.001)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()
    
def RescaleToTauID_2016():

    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_allbkgs
    uncs = uncertainties
    masses = utils.azh_masses
    variations = utils.variations
    signals = utils.azh_signals
    folder = utils.BaseFolder+'/root_files'
    print
    print('Scaling MC samples for updated tau ID scale factors in UL2016 samples')
    print('See recommendation in https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2')
    print

    for cat in cats:
        nameinput = folder + "/MC_data_"+cat+"_2016.root"
        inputfile = ROOT.TFile(nameinput,'update')
        for channel in channels:
            scale = tauID_UL2016[channel]
            print('scaling backgrounds for UL2016 in %s category of %s channel by TauID SF of %5.2f'%(cat,channel,scale))
            for template in templates:
                hist = inputfile.Get(channel+'/'+template)
                hist.Scale(scale)
                inputfile.cd(channel)
                hist.Write(template)
                for unc in uncs:
                    for variation in variations:
                        histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                        if histSys!=None:
                            histSys.Scale(scale)
                            inputfile.cd(channel)
                            histSys.Write(template+'_'+unc+variation)
        inputfile.Close()

        for mass in masses:
            nameinput = folder + "/signal_"+mass+"_"+cat+"_2016.root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
                scale = tauID_UL2016[channel]
                print('scaling signals for UL2016 in %s category of %s channel and mA=%s by TauID SF of %5.2f'
                      %(cat,channel,mass,scale))
                for template in signals:
                    hist = inputfile.Get(channel+'/'+template)
                    hist.Scale(scale)
                    inputfile.cd(channel)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                histSys.Scale(scale)
                                inputfile.cd(channel)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()
    
def SymmetrizeUnc(**kwargs):

    era = kwargs.get('year','2018')
    years = []
    if era=='Run2':        
        years = utils.years
    else:
        years.append(era)
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_allbkgs
    uncs = uncertainties
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    variations = utils.variations
    signals = utils.azh_signals

    for year in years:
        print('symmetrizing uncertainties for UL%s'%(year))
        for cat in cats:
            nameinput = folder + "/MC_data_"+cat+"_"+year+".root"
            inputfile = ROOT.TFile(nameinput,'update')
            for channel in channels:
                for template in templates:
                    hist = inputfile.Get(channel+'/'+template)
                    for unc in uncs:
                        hists = {}
                        hists['central'] = hist
                        hists['up'] = inputfile.Get(channel+'/'+template+'_'+unc+'Up')
                        hists['down'] = inputfile.Get(channel+'/'+template+'_'+unc+'Down')
                        if hists['up']!=None and hists['down']!=None:
                            utils.symmetrizeUnc(hists)
                            if unc=='eleES':
                                nbins = hist.GetNbinsX()
                                for ib in range(1,nbins+1):
                                    x = hist.GetBinContent(ib)
                                    xup = hists['up'].GetBinContent(ib)
                                    xdown = hists['down'].GetBinContent(ib)
                                    xup_new = x + 0.5*(xup-x)
                                    xdown_new = x + 0.5*(xdown-x)
                                    hists['up'].SetBinContent(ib,xup_new)
                                    hists['down'].SetBinContent(ib,xdown_new)
                            inputfile.cd(channel)
                            hists['up'].Write(template+'_'+unc+'Up')
                            hists['down'].Write(template+'_'+unc+'Down')
            inputfile.Close()

            for mass in masses:
                nameinput = folder + "/signal_"+mass+"_"+cat+"_"+year+".root"
                inputfile = ROOT.TFile(nameinput,'update')
                for channel in channels:
                    for template in signals:
                        hist = inputfile.Get(channel+'/'+template)
                        for unc in uncs:
                            hists = {}
                            hists['central'] = hist
                            hists['up'] = inputfile.Get(channel+'/'+template+'_'+unc+'Up')
                            hists['down'] = inputfile.Get(channel+'/'+template+'_'+unc+'Down')
                            if hists['up']!=None and hists['down']!=None:
                                utils.symmetrizeUnc(hists)
                                if unc=='eleES':
                                    nbins = hist.GetNbinsX()
                                    for ib in range(1,nbins+1):
                                        x = hist.GetBinContent(ib)
                                        xup = hists['up'].GetBinContent(ib)
                                        xdown = hists['down'].GetBinContent(ib)
                                        xup_new = x + 0.5*(xup-x)
                                        xdown_new = x + 0.5*(xdown-x)
                                        hists['up'].SetBinContent(ib,xup_new)
                                        hists['down'].SetBinContent(ib,xdown_new)
                                inputfile.cd(channel)
                                hists['up'].Write(template+'_'+unc+'Up')
                                hists['down'].Write(template+'_'+unc+'Down')
                inputfile.Close()

def ReducibleSystematics(**kwargs):

    era = kwargs.get('year','Run2')
    years = []
    print
    if era=='Run2':
        years = utils.years
    else:
        years.append(era)
    z_channels = ['ee','mm']
    h_channels = ['em','mt','et','tt']
    cats = utils.azh_cats
    for year in years:
        for cat in cats:
            rootname='%s/root_files/MC_data_%s_%s.root'%(utils.BaseFolder,cat,year)
            rootfile=ROOT.TFile(rootname,'update')
            if rootfile==None:
                print('file %s not found'%(rootname))
                exit(1)
            for z_channel in z_channels:
                for h_channel in h_channels:
                    channel = z_channel+h_channel                    
                    print('constructing systematics for reducible background : %s %s %s'%(year,cat,channel))
                    nameroot_reducible = '%s/root_files/%s_comb_m4l_cons_OS_%s.root'%(utils.BaseFolder,h_channel,year)
                    root_reducible = ROOT.TFile(nameroot_reducible)
                    if root_reducible==None:
                        print('file %s not found'%(root_reducible))
                        exit(1)
                    hist_os_app = root_reducible.Get('os_application') 
                    hist_reducible = root_reducible.Get('reducible')
                    name='%s_%s_%s'%(year,cat,channel)
                    hist_os_app_rebin = utils.rebinHisto(hist_os_app,utils.bins_fakes,name)
                    name='%s_%s_%s'%(year,cat,channel)
                    hist_reducible_rebin = utils.rebinHisto(hist_reducible,utils.bins_fakes,name)
                    name='sys_%s_%s_%s'%(year,cat,channel)
                    hist_sys=hist_os_app_rebin.Clone(name)
                    nbins_sys=hist_sys.GetNbinsX()
                    hist_fake = rootfile.Get(channel+'/reducible')

                    hist_fake_sys = {}
                    lower_edge=hist_sys.GetBinLowEdge(1)
                    upper_edge=hist_sys.GetBinLowEdge(nbins_sys+1)

                    for ib in range(1,nbins_sys+1):
                        error = hist_os_app_rebin.GetBinError(ib)
                        x_os_app = hist_os_app_rebin.GetBinContent(ib)
                        x_reducible = hist_reducible_rebin.GetBinContent(ib)
                        x_max = max(x_os_app,x_reducible)
                        maximal = max(x_max,error)
                        sys=1.0
                        if maximal>0:
                            sys=error/maximal                            
                        hist_sys.SetBinContent(ib,sys)
                        hist_sys.SetBinError(ib,0.)
                        binname='bin%1i'%(ib)
                        hist_sys.GetXaxis().SetBinLabel(ib,binname)
                        nameUp = 'reducible_'+binname+'Up'
                        nameDown = 'reducible_'+binname+'Down'
                        hist_fake_sys[nameUp] = hist_fake.Clone(nameUp)
                        hist_fake_sys[nameDown] = hist_fake.Clone(nameDown)

                    nbins=hist_fake.GetNbinsX()
                    for ib in range(1,nbins+1):
                        center = hist_fake.GetBinCenter(ib)
                        if center<lower_edge:
                            center = lower_edge + 0.1
                        if center>upper_edge:
                            center = upper_edge - 0.1
                        x = hist_fake.GetBinContent(ib)
                        bin_sys = hist_sys.FindBin(center)
                        binname = hist_sys.GetXaxis().GetBinLabel(bin_sys)
                        sys = hist_sys.GetBinContent(bin_sys)
                        x_down = max(0.,x/(1.0+sys))
                        x_up = max(0.,x*(1.0+sys))
                        nameUp = 'reducible_'+binname+'Up'
                        nameDown = 'reducible_'+binname+'Down'
                        hist_fake_sys[nameDown].SetBinContent(ib,x_down)
                        hist_fake_sys[nameUp].SetBinContent(ib,x_up)
                        
                    rootfile.cd(channel)
                    for hist in hist_fake_sys:
                        hist_fake_sys[hist].Write(hist)

                    root_reducible.Close()
            rootfile.Close()
    print
    print('done constructing systematics for reducible background')
    print

############
### MAIN ###
############
if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-year','--year',dest='year',default='Run2',help=""" year : 2016 2017 2018 Run2""",choices=utils.years_ext)
    parser.add_argument('-folder','--folder',dest='folder',default='coffea',help=""" folder with ROOT files""")
    parser.add_argument('-binning','--binning',dest='binning',default='nominal',help=""" binning """,choices=['nominal','fine','coarse'])
    args = parser.parse_args()

    ROOT.gROOT.SetBatch(True)

    RebinAndSave(folder=args.folder,year=args.year,binning=args.binning)

    # fixing bins with negative content
    FixNegativeBins(year=args.year)

    # rescale MC shapes by new tau ID
    if args.year=='Run2' or args.year=='2016':
        RescaleToTauID_2016()

    # symmetrize shape uncertainties
    SymmetrizeUnc(year=args.year)

    # constructing systematic templates 
    # for reducible background (obsolete)
    # ReducibleSystematics(year=args.year)

    # creating folders for figures, batch jobs
    pathdir=utils.BaseFolder+'/figures'
    if not os.path.isdir(pathdir): os.system('mkdir figures')
    pathdir=utils.BaseFolder+'/jobs'
    if not os.path.isdir(pathdir): os.system('mkdir jobs')
