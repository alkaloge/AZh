#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandImpacts(**kwargs):
    
    typ = kwargs.get('typ','exp')
    proc = kwargs.get('proc','ggA')
    mass = kwargs.get('mass','400')
    strategy = kwargs.get('strategy',1)
    r_ggA = kwargs.get('r_ggA','1')
    r_bbA = kwargs.get('r_bbA','0')
    
    if typ not in ['exp','obs']:
        print('warning : ill-specified type of computation : %s'%(typ))
        print('available options : exp, obs')
    expect = False
    if typ=='exp':
        expect = True

    otherProcess = 'bbA'
    if proc=='bbA':
        otherProcess = 'ggA'

    # change to dir where output will be stored
    command = 'cd %s/impacts_%s%s_%s ; '%(utils.BaseFolder,proc,mass,typ)
    # perform initial fit and perform likelihood scan for signal strength
    command += 'combineTool.py -M Impacts -d %s/datacards/Run2/%s/ws.root -m %s '%(utils.BaseFolder,mass,mass)
    command += '--robustFit 1 --cminDefaultMinimizerTolerance 0.05 '
    command += '--X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO '
    command += '--cminDefaultMinimizerStrategy %1i '%(strategy)
    command += '--setParameterRanges r_ggA=-20,20:r_bbA=-20,20 '
    command += '--freezeParameters r_%s '%(otherProcess)
    if expect:
        command += '-t -1 '
    command += '--setParameters r_ggA=%s,r_bbA=%s '%(r_ggA,r_bbA)
    command += '--redefineSignalPOIs r_%s '%(proc)
    command += '--doInitialFit ; '
    # run scans of all nuisances; submit jobs to the local batch system
    command += 'combineTool.py -M Impacts -d %s/datacards/Run2/%s/ws.root -m %s '%(utils.BaseFolder,mass,mass)
    command += '--robustFit 1 --cminDefaultMinimizerTolerance 0.05 '
    command += '--X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO '
    command += '--cminDefaultMinimizerStrategy %1i '%(strategy)
    command += '--setParameterRanges r_ggA=-20,20:r_bbA=-20,20 '
    command += '--freezeParameters r_%s '%(otherProcess)
    if expect:
        command += '-t -1 '
    command += '--setParameters r_ggA=%s,r_bbA=%s '%(r_ggA,r_bbA)
    command += '--redefineSignalPOIs r_%s '%(proc)
    command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --merge 4 --doFits ; '
    # return to the original folder
    command += 'cd ../'

    return command

#############################################

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses)
    parser.add_argument('-obs','--obs',dest='obs',action='store_true')
    parser.add_argument('-r_ggA','--r_ggA',dest='r_ggA',type=float,default=1.0)
    parser.add_argument('-r_bbA','--r_bbA',dest='r_bbA',type=float,default=0.0)
    parser.add_argument('-minimizer_strategy','--minimizer_strategy',dest='strategy',type=int,default=1)
    args = parser.parse_args()

    typ='exp'
    if args.obs: 
        typ='obs'

    strategy=args.strategy
    proc=args.proc
    mass=args.mass
    r_ggA=args.r_ggA
    r_bbA=args.r_bbA

    folder='%s/impacts_%s%s_%s'%(utils.BaseFolder,proc,mass,typ)
    if os.path.isdir(folder):
        os.system('rm %s/*'%(folder))
    else:
        print('Creating folder %s'%(folder))
        os.system('mkdir %s'%(folder))
    command = MakeCommandImpacts(
        proc=proc,
        mass=mass,
        typ=typ,
        strategy=strategy,
        r_ggA=r_ggA,
        r_bbA=r_bbA)
    os.system(command)


