#!/usr/bin/env python
import os

##############################
# Main routine
##############################
if __name__ == "__main__":


    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-sample','--sample',dest='sample',type=str,required=True)
    parser.add_argument('-mass','--mass',dest='mass',type=str,required=True)
    parser.add_argument('-proc','--proc',dest='proc',default='bbA')
    parser.add_argument('-minimizer','--minimizer',dest='minimizer',default='0')
    parser.add_argument('-xmin','--xmin',dest='xmin',default='-5.0')
    parser.add_argument('-xmax','--xmax',dest='xmax',default='5.0')
    parser.add_argument('-npoints','--npoints',dest='npoints',default='101')
    
    args = parser.parse_args()
    otherProc = 'ggA'
    if args.proc=='ggA':
        otherProc = 'bbA'

    command = 'ulimit -s unlimited ; '
    command += 'combineTool.py -m %s -M MultiDimFit -P r_%s '%(args.mass,args.proc)
    command += '--setParameterRanges r_%s=%s,%s '%(args.proc,args.xmin,args.xmax)
    command += '--setParameters r_%s=0 '%(otherProc)
    command += '--freezeParameters r_%s '%(otherProc)
    command += '--floatOtherPOIs 1 --points %s '%(args.npoints) 
    command += '--cminDefaultMinimizerTolerance 0.01 '
    command += '--robustFit 1 -d datacards/%s/%s/ws.root '%(args.sample,args.mass) 
    command += '--algo grid --alignEdges 1 --cminDefaultMinimizerStrategy %s -n _%s_%s ; '%(args.minimizer,args.sample,args.proc)
    command += 'plot1DScan.py higgsCombine_%s_%s.MultiDimFit.mH%s.root --POI r_%s --output scan_%s_%s%s'%(args.sample,args.proc,args.mass,args.proc,args.sample,args.proc,args.mass)
    os.system(command)
