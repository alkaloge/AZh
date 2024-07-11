#!/usr/bin/env python3

import os
import AZh.combine.utilsAZh as utils

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('-sample','--sample',dest='sample',required=True,choices=['2016','2017','2018','Run2','et','mt','tt','em'])
parser.add_argument('-indir','--indir',dest='indir',required=True,help=""" output folder where results of limits are stored""")
parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses_ext)
parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
parser.add_argument('-quantile','--quantile',dest='quantile',default='obs')
parser.add_argument('-folder','--folder',dest='folder',default='datacards')
args = parser.parse_args()

inputFolder = utils.BaseFolder + '/' + args.indir
datacardsFolder = utils.BaseFolder + '/' + args.folder + '_' + args.proc
datacardsFilename = '%s/%s/%s/ws.root'%(datacardsFolder,args.sample,args.mass)

command = 'cd %s ; '%(inputFolder)
command += 'combine -d %s -m %s '%(datacardsFilename,args.mass) 
command += '-M HybridNew --LHCmode LHC-limits --readHybridResults '
if args.quantile!='obs':
    command += '--expectedFromGrid=%s '%(args.quantile)
    
gridFile = '%s/limit_%s_%s_%s.root '%(inputFolder,args.sample,args.proc,args.mass)
command += ' --grid=%s ; '%(gridFile)
command += 'cd - '
os.system(command)
