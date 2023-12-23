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

def MergeDataMC():
    os.system('cp root_files/backup/*root root_files')
    os.system('./Hadd_MC_data.bash')

def FixNegativeBins():

    years = utils.years
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    uncs = utils.azh_uncs
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
                        if x<0:
                            print('negative bin %2i :  %7.5f in %s_%s_%s %s'
                                  %(ib,x,year,cat,channel,template))
                            hist.SetBinContent(ib,0.)
                            hist.SetBinError(ib,0.)
                    inputfile.cd(channel)
                    hist.Write(template)
                    for unc in uncs:
                        for variation in variations:
                            histSys = inputfile.Get(channel+'/'+template+'_'+unc+variation)
                            if histSys!=None:
                                for ib in range(1,nbins+1):
                                    x = histSys.GetBinContent(ib)
                                    if x<0:
                                        print('negative bin %2i : %7.5f in %s_%s_%s %s_%s%s'
                                              %(ib,x,year,cat,channel,template,unc,variation))
                                        histSys.SetBinContent(ib,0.)
                                        histSys.SetBinError(ib,0.)
                                inputfile.cd(channel)
                                histSys.Write(template+'_'+unc+variation)
            inputfile.Close()
    
def RescaleToTauID_2016():

    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    uncs = utils.azh_uncs
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
    
def SymmetrizeUnc():

    years = utils.years
    cats = utils.azh_cats
    channels = utils.azh_channels
    templates = utils.azh_bkgs
    uncs = utils.azh_uncs
    masses = utils.azh_masses
    folder = utils.BaseFolder+'/root_files'
    variations = utils.variations
    signals = utils.azh_signals

    for year in years:
        print('symmetrizing bkg uncertainties for UL%s'%(year))
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
                                inputfile.cd(channel)
                                hists['up'].Write(template+'_'+unc+'Up')
                                hists['down'].Write(template+'_'+unc+'Down')
                inputfile.Close()

def ReducibleSystematics():

    print
    years = utils.years
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


    ROOT.gROOT.SetBatch(True)

    # merging data and MC into one file
    MergeDataMC()

    # fixing bins with negative content
    FixNegativeBins()

    # rescale MC shapes by new tau ID
    RescaleToTauID_2016()

    # symmetrize shape uncertainties
    SymmetrizeUnc()

    # constructing systematic templates 
    # for reducible background
    ReducibleSystematics()

    # creating folders for figures, batch jobs
    pathdir=utils.BaseFolder+'/figures'
    if not os.path.isdir(pathdir): os.system('mkdir figures')
    pathdir=utils.BaseFolder+'/jobs'
    if not os.path.isdir(pathdir): os.system('mkdir jobs')
