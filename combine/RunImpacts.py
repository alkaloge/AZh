#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandImpacts(**kwargs):
    

    typ = kwargs.get('typ','exp')
    proc = kwargs.get('proc','ggA')
    mass = kwargs.get('mass','400')
    strategy = kwargs.get('strategy',1)
    r_ggA = kwargs.get('r_ggA','0')
    r_bbA = kwargs.get('r_bbA','0')
    
    expect = False
    if typ.lower() in 'expcted':
        expect = True

    # change to dir where output will be stored
    command = 'cd %s_impacts_%s%s ; '%(typ,proc,mass)
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


if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-proc','--proc',dest='proc',default='ggA')
    parser.add_argument('-mass','--mass',dest='mass',default='1000')
    parser.add_argument('-typ','--typ',dest='typ',default='exp')
    parser.add_argument('-r_ggA','--r_ggA',dest='r_ggA',type=float,default=0.0)
    parser.add_argument('-r_bbA','--r_bbA',dest='r_bbA',type=float,default=1.0)
    parser.add_argument('-minimizer_strategy','--Minimizer_strategy',dest='strategy',type=int,default=1)
    args = parser.parse_args()

    typ = args.typ
    if typ.lower() not in ['exp','obs']:
        print('Unavailable option of parameter --typ',typ)
        print('should be exp or obs')
        exit(1)

    folder='%s/%s_impacts_%s%s'%(utils.BaseFolder,args.typ,args.proc,args.mass)
    if os.path.isdir(folder):
        os.system('rm %s/*'%(folder))
    else:
        print('Creating folder %s'%(folder))
        os.system('mkdir %s'%(folder))
    
    
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


