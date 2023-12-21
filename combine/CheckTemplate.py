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
    parser.add_argument('-sys','--sys',dest='sys',default='all')
    parser.add_argument('-mass','--mass',dest='mass',default='300')
    parser.add_argument('-xmin','--xmin',dest='xmin',type=float,default=200)
    parser.add_argument('-xmax','--xmax',dest='xmax',type=float,default=1000)
    parser.add_argument('-logx','--logx',dest='logx',action='store_true')
    parser.add_argument('-dry_run','--dry_run',dest='dry_run',action='store_true')
    parser.add_argument('-printout','--printout',dest='verbosity',action='store_true')

    args = parser.parse_args()

    analysis = args.analysis
    year = args.year
    cat = args.cat
    channel = args.chan
    templ = args.templ
    sys = args.sys
    mass = args.mass
    xmin = args.xmin
    xmax = args.xmax

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
        print('--xmin : minimum boundary of x axis (default=200)')
        print('--xmax : maximum boundary of x axis (default=1000')
        print('--logx : set x axis to logarithmic scale')
        print('--verbosity : detailed printout')
        print('--dry_run : dry run with printout of available options')
        print
        print('Specific info for analysis %s -> '%(analysis))
        xmasses = utils.hig18023_massses
        xtemplates = utils.hig18023_bkgs
        xtemplates.append('ggA')
        xuncs = utils.hig18023_uncs
        if analysis=='azh':
            xmasses = utils.azh_massses
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
    uncs = []
    unc_postfix = ''

    analysis_type = 0

    if sys.lower()=='all':
        uncs = utils.azh_uncs
    else:
        uncs = [sys]

    if templ.lower()=='all':
        templates = utils.azh_bkgs
        templates.remove('reducible')
    else:
        templates = [templ]

    if analysis.lower()=='azh':
        analysis_type = 1
        folder = os.getenv('CMSSW_BASE') + '/src/AZh/combine/datacards/Run2/'+mass
        filename = 'azh_'+year+'_'+cat+'_'+channel+'_'+mass+'.root'
        unc_postfix = '_'+year
        if templ.lower()=='all':
            for sig in utils.azh_signals:
                templates.append(sig+mass)
    if analysis.lower()=='hig18023':
        analysis_type = 2
        if sys.lower()=='all':
            uncs = utils.hig18023_uncs
        if templ.lower()=='all':
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


    for xt in templates:
        template=xt
        if templ=='bbA' or templ=='ggA' or templ=='AZH':
            if analysis_type>0: template += mass
        hist = inputfile.Get(dirname+prefix+template)
        if hist==None:
            print('template %s not found in folder %s'%(template,dirname))
            continue
        for unc in uncs:
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
                               logx=False)


    print
    print
    print('year = %s : category = %s : channel = %s'%(year,cat,channel))
    print('plots are produced for templates ',templates)
    print('and systematic uncertainties ',uncs)
    print('from input file : %s'%(fullfilename))
    print('output figures are put put in the folder %s'%(utils.FiguresFolder))
    print
