#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandPlot(**kwargs):

    proc = kwargs.get('proc','ggA')
    mass = kwargs.get('mass','300')
    typ = kwargs.get('typ','exp')
    blind = kwargs.get('blind',True)

    otherProc = 'bbA'
    if proc=='bbA':
        otherProc = 'ggA'

    folder = '%s/impacts_%s%s_%s'%(utils.BaseFolder,proc,mass,typ)
    command = 'cd %s ; '%(folder)
    # creating plots with other POI
    command += 'combineTool.py -M Impacts -d %s/datacards/Run2/%s/ws.root -m %s '%(utils.BaseFolder,mass,mass)
    command += '--redefineSignalPOIs r_%s -m %s -o impacts.json ; '%(proc,mass)
    command += 'plotImpacts.py -i impacts.json -o impacts ' 
    if blind and typ=='obs':
        command += ' --blind '
    # creating plots w/o other POI
    command += ' ; mv higgsCombine_paramFit_Test_r_%s.MultiDimFit.mH%s.root backup.xxx '%(otherProc,mass)
    command += ' ; combineTool.py -M Impacts -d %s/datacards/Run2/%s/ws.root -m %s '%(utils.BaseFolder,mass,mass)
    command += '--redefineSignalPOIs r_%s -m %s -o impacts_noOtherPOI.json'%(proc,mass)
    command += ' ; plotImpacts.py -i impacts_noOtherPOI.json -o impacts_noOtherPOI ' 
    if blind and typ=='obs':
        command += ' --blind '
    command += ' ; mv backup.xxx higgsCombine_paramFit_Test_r_%s.MultiDimFit.mH%s.root '%(otherProc,mass)

    command += ' ; cd - '

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses)
    parser.add_argument('-obs','--obs',dest='obs',action='store_true')
    parser.add_argument('-unblind','--unblind',dest='unblind',action='store_true')
    args = parser.parse_args()

    typ='exp'
    if args.obs: 
        typ='obs'

    proc=args.proc
    mass=args.mass
    blind = True
    if args.unblind:
        blind = False

    folder='%s/impacts_%s%s_%s'%(utils.BaseFolder,proc,mass,typ)
    if not os.path.isdir(folder):
        print(folder)
        print('folder does not exist !')
        print('Please check input parameters of PlotImpacts.py')
        if args.obs:
            print('Or execute first  RunImpacts.py --proc %s --mass %s --obs'%(proc,mass))
        else:
            print('Or execute first  RunImpacts.py --proc %s --mass %s'%(proc,mass))
        exit(1)
    command = MakeCommandPlot(proc=proc,mass=mass,typ=typ,blind=blind)
    print('executing')
    print(command)
    os.system(command)
    print

