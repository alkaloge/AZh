#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandImpacts(**kwargs):
    
    year = kwargs.get('year','Run2')
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

    # change to dir where output will be stored
    command = 'cd impacts_%s_%s%s_%s ; '%(year,proc,mass,typ)
    # perform initial fit and perform likelihood scan for signal strength
    command += 'combineTool.py -M Impacts -d %s/datacards/Run2/%s/ws.root -m %s '%(utils.BaseFolder,mass,mass)
    command += '--robustFit 1 --cminDefaultMinimizerTolerance 0.05 '
    command += '--X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO '
    command += '--cminDefaultMinimizerStrategy %1i '%(strategy)
    command += '--setParameterRanges r_ggA=-20,20:r_bbA=-20,20 '
    if expect:
        command += '-t -1 '%(strength)
        command += '--setParameters r_ggA=%s,r_bbA=%s '%(r_ggA,r_bbA)
    command += 'redefineSignalPOIs %s '%(proc)
    command += '--doInitialFit ; '
    # run scans of all nuisances; submit jobs to the local batch system
    command += 'combineTool.py -M Impacts -d %s/datacards_%s/Run2/%s/ws.root -m %s '%(utils.BaseFolder,proc,mass,mass)
    command += '--robustFit 1 --cminDefaultMinimizerTolerance 0.05 '
    command += '--X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO '
    command += '--cminDefaultMinimizerStrategy %1i '%(strategy)
    if expect:
        command += '-t -1 '%(strength)
        command += '--setParameters r_ggA=%s,r_bbA=%s '%(r_ggA,r_bbA)
    command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' ----merge 4 --doFits ; '%(jobdir)
    # return to the original folder
    command += 'cd ../'

    return command

def MakeCommandPlot(**kwargs):
    pro


if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses)
    parser.add_argument('-obs','--obs',dest='obs',action='store_true')
    parser.add_argument('-r_ggA','--r_ggA',dest='r_ggA',type=float,default=0.0)
    parser.add_argument('-r_bbA','--r_bbA',dest='r_bbA',type=float,default=1.0)
    parser.add_argument('-minimizer_strategy','--Minimizer_strategy',dest='strategy',type=int,default=1)
    parser.add_argument('-plot','--plot',dest='plot',action='store_true')
    args = parser.parse_args()

    typ='exp'
    if args.obs: 
        typ='obs'
    
    proc=args.proc
    mass=args.mass

    plot=False
    if args.plot:
        plot=True

    folder='%s/%s_impacts_%s%s'%(utils.BaseFolder,typ,proc,mass)
    if os.path.isdir(folder):
        os.system('rm %s/*'%(folder))
    else:
        print('Creating folder %s'%(folder))
        os.system('mkdir %s'%(folder))
    

    if plot:
    command = MakeCommandPlot()

    
    command = MakeCommandImpacts(
        proc=args.proc,
        mass=args.mass,
        typ=args.typ,
        strategy=args.strategy,
        strength=args.strength,
        r_ggA=args.rMin,
        r_bbA=args.rMax)
    
    #print(command)
    os.system(command)


