#!/usr/bin/env python3

import os
import ROOT
import AZh.combine.utilsAZh as utils
import numpy as np

def MakeCommand(**kwargs):

    sample = kwargs.get('sample','Run2')
    r_ggA = kwargs.get('r_ggA','5')
    r_bbA = kwargs.get('r_bbA','5')
    npoints = kwargs.get('npoints','10000')
    npoints_per_job = kwargs.get('npoints_per_job','100')
    mass = kwargs.get('mass','300')
    folder = kwargs.get('folder','datacards')
    batch = kwargs.get('batch',True)

    indir = '%s/%s/%s/%s'%(utils.BaseFolder,folder,sample,mass)
    dirname = '%s/2Dscan_%s_%s'%(utils.BaseFolder,sample,mass)

    command = 'cd %s ; '%(dirname)
    command += 'ulimit -s unlimited ; ';
    for typ in ['exp','obs']:
        command += 'combineTool.py -M MultiDimFit -m %s '%(mass) 
        command += '%s/ws.root '%(indir)
        #    command += '--redefineSignalPOIs r_ggA,r_bbA '
        command += '--setParameterRanges r_bbA=0,%s:r_ggA=0,%s '%(r_bbA,r_ggA)
        command += '--algo=grid --points=%s '%(npoints) 
        command += '--setParameters r_bbA=0,r_ggA=0 '
        command += '--robustFit 1 --cminDefaultMinimizerTolerance 0.1 '
        command += '--cminDefaultMinimizerStrategy=1 --X-rtd MINIMIZER_analytic -n .2Dscan_%s -v2 '%(typ)
        if typ=='exp':
            command += '-t -1 '
        if batch:
            taskname='2Dscan_%s_%s_%s'%(sample,mass,typ);
            command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s --split-points %s '%(taskname,npoints_per_job)
        command += ' ; '

    command += ' cd %s'%(utils.BaseFolder)
    return command


if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-sample','--sample',dest='sample',default='Run2',choices=['2016','2017','2018','Run2','et','mt','tt'])
    parser.add_argument('-mass','--mass',dest='mass',type=str,required=True)
    parser.add_argument('-folder','--folder',dest='folder',default='datacards',help=""" input folder twith datacards""")
    parser.add_argument('-r_ggA','--r_ggA',dest='r_ggA',default='10',help=""" Maximum of r_ggA """)
    parser.add_argument('-r_bbA','--r_bbA',dest='r_bbA',default='10',help=""" Maximum of r_bbA """)
    parser.add_argument('-npoints','--npoints',dest='npoints',default='200',help=""" number of points per POI""")
    parser.add_argument('-npoints_per_job','--npoints_per_job',dest='npoints_per_job',default='200',help=""" number of points per POI""")
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    name = "2Dscan_%s_%s"%(args.sample,args.mass)
    dirname = '%s/%s'%(utils.BaseFolder,name)
    ws = '%s/%s/%s/%s/ws.root'%(utils.BaseFolder,args.folder,args.sample,args.mass)
    if os.path.isdir(dirname):
        print('cleaning folder %s'%(dirname))
        os.system('rm %s/*'%(dirname))
    else:
        print ('creating folder %s'%(dirname))
        os.system('mkdir %s'%(dirname))

    if os.path.isfile(ws):
        print('running 2D scan on %s'%(ws))
    else:
        print('Workspace does not exist : %s'%(ws))
        exit()

    print('')

    rootFile = ROOT.TFile('Info_2D.root','recreate')
    rootFile.cd("")
    tree = ROOT.TTree('info','Info')
    npoints = np.zeros(1,dtype='i')
    ggA_max = np.zeros(1,dtype='d')
    bbA_max = np.zeros(1,dtype='d')
    tree.Branch('npoints',npoints,'npoints/I')
    tree.Branch('ggA_max',ggA_max,'ggA_max/D')
    tree.Branch('bbA_max',bbA_max,'bbA_max/D')
    npoints[0] = int(args.npoints)
    ggA_max[0] = float(args.r_ggA)
    bbA_max[0] = float(args.r_bbA)
    tree.Fill()
    tree.Write()
    rootFile.Close()
    os.system('mv Info_2D.root %s/'%(dirname))

    npoints2=str(int(args.npoints)*int(args.npoints))
    command = MakeCommand(sample=args.sample,
                          r_ggA=args.r_ggA,
                          r_bbA=args.r_bbA,
                          npoints=npoints2,
                          npoints_per_job=args.npoints_per_job,
                          mass=args.mass,
                          folder=args.folder,
                          batch=args.batch)
    print(command)
    os.system(command)
