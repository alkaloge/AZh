#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandFit(**kwargs):

    sample = kwargs.get('sample','Run')
    mass = kwargs.get('mass','300')
    batch = kwargs.get('batch',True)
    expected = kwargs.get('expected',True)
    robustHesse = kwargs.get('robustHesse',True)
    saveShapes = kwargs.get('saveShapes',True)
    folder =  kwargs.get('folder','datacards')
    minimizer = kwargs.get('minimizer','1')
    r_ggA = kwargs.get('r_ggA','0')
    r_bbA = kwargs.get('r_ggA','0')
    proc = kwargs.get('proc','ggA')
    typ = 'obs'
    otherProcess = 'bbA'
    if proc=='bbA':
        otherProcess = 'ggA'
    if expected:
        typ = 'exp'

    command = 'cd %s/fit_%s_mA%s_%s ; '%(utils.BaseFolder,sample,mass,typ) 
    command += 'combineTool.py -M FitDiagnostics'
    command += ' -d %s/%s/%s/%s/ws.root'%(utils.BaseFolder,folder,sample,mass)
    if saveShapes:
        command += ' --saveNormalizations --saveShapes --saveWithUncertainties'
    if robustHesse:
        command += ' --robustHesse 1'
    else:
        command += ' --robustFit 1'
    if expected:
        command += ' -t -1'
    command += ' --setParameters r_ggA=%s,r_bbA=%s'%(r_ggA,r_bbA) 
    command += ' --setParameterRanges r_%s=-10,10 '%(proc)
    command += ' --redefineSignalPOIs r_%s '%(proc)
    command += ' --freezeParameters r_%s '%(otherProcess)
    command += ' --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO '
    command += ' --cminDefaultMinimizerStrategy=%s -m %s'%(minimizer,mass)
    if batch:
        taskname='fit_%s_mA%s_%s'%(sample,mass,typ);
        command += ' --job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s '%(taskname)
    else:
        command += ' -v3 >> output.txt'
    command += ' ; cd -'

    return command


#############################################

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-sample','--sample',dest='sample',default='Run2')
    parser.add_argument('-mass','--mass',dest='mass',default='300',choices=utils.azh_masses)
    parser.add_argument('-obs','--obs',dest='obs',action='store_true')
    parser.add_argument('-r_ggA','--r_ggA',dest='r_ggA',default='0')
    parser.add_argument('-r_bbA','--r_bbA',dest='r_bbA',default='0')
    parser.add_argument('-proc','--proc',dest='proc',default='ggA')
    parser.add_argument('-folder','--folder',dest='folder',default='datacards')
    parser.add_argument('-saveShapes','--saveShapes',dest='saveShapes',action='store_true')
    parser.add_argument('-robustHesse','--robustHesse',dest='robustHesse',action='store_true')
    parser.add_argument('-minimizer','--minimizer',dest='minimizer',default='0')
    parser.add_argument('-batch','--batch',action='store_true')
    args = parser.parse_args()

    expected = not args.obs
    typ = 'obs'
    if expected:
        typ = 'exp'

    outdir = '%s/fit_%s_mA%s_%s'%(utils.BaseFolder,args.sample,args.mass,typ) 
    if not os.path.isdir(outdir):
        os.system('mkdir %s'%(outdir)) 

    command = MakeCommandFit(
        sample=args.sample,
        mass=args.mass,
        batch=args.batch,
        expected=expected,
        robustHesse=args.robustHesse,
        saveShapes=args.saveShapes,
        folder=args.folder,
        minimizer=args.minimizer,
        proc=args.proc,
        r_ggA=args.r_ggA,
        r_bbA=args.r_bbA
    )
    print(command)
    os.system(command)
