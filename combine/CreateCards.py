#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils
import argparse

###### main ############
if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-year','--year',dest='year',required=True,choices=['2016','2017','2018','all'])
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses_ext)
    parser.add_argument('-model','--model',dest='model',default='2POI',choices=['ggA','bbA','2POI'])
    parser.add_argument('-all_channels','--all_channels',action='store_true')
    parser.add_argument('-folder','--folder',dest='folder',default='datacards')
    args = parser.parse_args()

    channels = ['et','mt','tt']
    cats = ['btag','0btag']
    if args.all_channels:
        channels.append('em')
    folder = args.folder
    proc = args.model
    years = []
    if args.year=='all':
        years = utils.years
    else:
        years.append(args.year)
    cats = utils.azh_cats

    masses = [] 
    if args.mass=='all':
        masses = utils.azh_masses
    else:
        masses.append(args.mass)

    for year in years:
        for mass in masses:
            for cat in cats:
                command = 'make_datacards.py --year %s --btag %s --mass %s --model %s --folder %s'%(year,cat,mass,proc,folder)
                if args.all_channels:
                    command += ' --all_channels '
                full_command = utils.BaseFolder+'/'+command
                print(command)
                os.system(full_command)

    for channel in channels:
        if not os.path.isdir('%s/%s'%(folder,channel)):
             os.system('mkdir %s/%s'%(folder,channel))
        for mass in masses:
            if not os.path.isdir('%s/%s/%s'%(folder,channel,mass)):
                os.system('mkdir %s/%s/%s'%(folder,channel,mass))
            source = folder+'/Run2/'+mass+"/*ee"+channel+"*"
            target = folder+'/'+channel+'/'+mass
            os.system('cp '+source+' '+target)
            source = folder+'/Run2/'+mass+"/*mm"+channel+"*"
            target = folder+'/'+channel+'/'+mass
            os.system('cp '+source+' '+target)
    for cat in cats:
        if not os.path.isdir('%s/%s'%(folder,cat)):
             os.system('mkdir %s/%s'%(folder,cat))
        for mass in masses:
            if not os.path.isdir('%s/%s/%s'%(folder,cat,mass)):
                os.system('mkdir %s/%s/%s'%(folder,cat,mass))
                source = folder+'/Run2/'+mass+'/*_'+cat+'*'
                target = folder+'/'+cat+'/'+mass
                os.system('cp '+source+' '+target)
        
    print
    print('datacards are written to folder %s '%(folder))
