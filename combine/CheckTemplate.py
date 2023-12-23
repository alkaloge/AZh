#!/usr/bin/env python

import AZh.combine.stylesAZh as styles
import AZh.combine.utilsAZh as utils
import argparse
import ROOT
import os

############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    parser = argparse.ArgumentParser(description="Check datacards")

    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh',choices=['azh','hig18023','root'])
    parser.add_argument('-year','--year',dest='year',default='2018',choices=['2016','2017','2018'])
    parser.add_argument('-cat','--cat',dest='cat',default='0btag',choices=['0btag','btag'])
    parser.add_argument('-channel','--channel',dest='chan',default='mmtt',choices=utils.azh_channels)
    parser.add_argument('-template','--template',dest='templ',default='all')
    parser.add_argument('-mass','--mass',dest='mass',default='300')
    parser.add_argument('-xmin','--xmin',dest='xmin',type=float,default=200)
    parser.add_argument('-xmax','--xmax',dest='xmax',type=float,default=2000)
    parser.add_argument('-logx','--logx',dest='logx',action='store_true')
    parser.add_argument('-dry_run','--dry_run',dest='dry_run',action='store_true')
    parser.add_argument('-printout','--printout',dest='verbosity',action='store_true')

    args = parser.parse_args()

    analysis = args.analysis
    year = args.year
    cat = args.cat
    channel = args.chan
    templ = args.templ
    mass = args.mass
    xmin = args.xmin
    xmax = args.xmax
    logx = args.logx

    verbosity=False
    if args.verbosity: 
        verbosity=True

    analyses = ['azh','hig18023']
    
    if args.dry_run:
        print
        print('Dry run of CheckTemplate.py')
        print('Arguments ')
        print('--analysis : ',analyses)
        print('--cat : ',utils.azh_cats)
        print('--channel : ',utils.azh_channels)
        print('--xmin : %s'%('minimum boundary of x axis (default=200)'))
        print('--xmax : %s'%('maximum boundary of x axis (default=1000'))
        print('--logx : %s'%('set x axis to logarithmic scale'))
        print('--verbosity : %s'%('detailed printout'))
        print('--dry_run : %s'%('dry run with printout of available options'))
        print
        print('Specific info for analysis %s -> '%(analysis))
        xmasses = utils.hig18023_masses
        xtemplates = utils.hig18023_bkgs
        xtemplates.append('ggA')
        xuncs = utils.hig18023_uncs
        if analysis=='azh':
            xmasses = utils.azh_masses
            xtemplates = utils.azh_bkgs
            xtemplates.append(['ggA','bbA'])
            xuncs = utils.azh_uncs

        print('--masses : ',xmasses)
        print('--templates : ',xtemplates)
        print('--sys : ',xuncs) 
        exit(1)


    folder = utils.BaseFolder+'/root_files'
    filename = 'MC_data_'+cat+'_'+year+'.root'
    dirname = channel+'/'
    prefix = ''
    
    templates = []
    uncs = utils.azh_uncs
    fake_uncs = utils.azh_fakeuncs
    unc_postfix = ''
    higgs_chan = utils.azh_higgs_channels[channel]

    analysis_type = 0

    if templ=='all':
        templates = utils.azh_bkgs
    else:
        templates = [templ]

    if analysis=='root':
        fake_uncs = ['bin1','bin2','bin3']
    elif analysis=='azh':
        analysis_type = 1
        folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/datacards/Run2/'+mass
        filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
        unc_postfix = '_'+year
        fake_uncs = [higgs_chan+'_bin1',higgs_chan+'_bin2',higgs_chan+'_bin3']
        if templ=='all':
            for sig in utils.azh_signals:
                templates.append(sig+mass)
    if analysis.lower()=='hig18023':
        analysis_type = 2
        uncs = utils.hig18023_uncs
        if templ.lower=='all':
            templates = utils.hig18023_bkgs
            templates.remove('data_FR')
            templates.append('AZH'+mass)
        folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/HIG-18-023/datacards/'+utils.hig18023_channels[channel]+'/Aconstr_HsvFit90/common'
        filename = 'SR.input.root'
        prefix = 'x_' 
        dirname = ''


    if verbosity:
        print
        print('templates  = ',templates)
        print('uncertainties = ',uncs)
        print

    fullfilename = folder+'/'+filename
    inputfile = ROOT.TFile(fullfilename)
    if verbosity:
        print('opening file %s',fullfilename)
    if inputfile==None:
        print('file %s not found'%(fullfilename))
        exit(1)

    print
    for xt in templates:
        template=xt
        if templ=='bbA' or templ=='ggA' or templ=='AZH':
            if analysis_type>0: template += mass
        hist = inputfile.Get(dirname+prefix+template)
        if hist==None:
            print('template %s not found in folder %s'%(template,dirname))
            continue
        systematics=uncs
        if xt=='reducible':
            if analysis=='root' or analysis=='azh':
                systematics=fake_uncs
            
        for unc in systematics:
            histUp = hist
            histDown = hist
            if unc.lower()!='none':
                histUp = inputfile.Get(dirname+prefix+template+'_'+unc+unc_postfix+'Up')
                histDown = inputfile.Get(dirname+prefix+template+'_'+unc+unc_postfix+'Down')
            if histUp==None or histDown==None:
                print('template %s with systematics %s not found'%(template,unc))
                continue
            hists = {}
            hists['central'] = hist
            hists['up'] = histUp
            hists['down'] = histDown
            utils.PlotTemplate(hists,
                               analysis=analysis,
                               year=year,
                               cat=cat,
                               channel=channel,
                               templ=template,
                               sys=unc,
                               verbosity=verbosity,
                               xmin=xmin,
                               xmax=xmax,
                               logx=logx)


    print
    print('year = %s : category = %s : channel = %s'%(year,cat,channel))
    print('plots are produced for templates ',templates)
    print('uncertainties in MC samples  ',uncs)
    if analysis=='root' or analysis=='azh':
        print('uncertainties in reducible background ',fake_uncs)
    print('input RooT file : %s'%(fullfilename))
    print('output figures are put put in the folder %s'%(utils.FiguresFolder))
    print
