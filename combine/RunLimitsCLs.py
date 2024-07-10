#!/usr/bin/env python3

import os
import AZh.combine.utilsAZh as utils

def MakeCommand(**kwargs):

    outdir = kwargs.get('outdir','limits_cls')
    sample = kwargs.get('sample','Run2')
    proc = kwargs.get('proc','ggA')
    mass = kwargs.get('mass','1000')
    batch = kwargs.get('batch',False)
    folder = kwargs.get('folder','datacards')
    strength = kwargs.get('strength','0.5')
    ntoys = kwargs.get('ntoys','100')
    indir = utils.BaseFolder + '/' + folder

    fullpath_out = utils.BaseFolder+'/'+outdir
    command = 'cd %s ; '%(fullpath_out)
    command += 'combineTool.py -M HybridNew --LHCmode LHC-limits ' 
    command += '--singlePoint %s '%(strength)
    command += '-d %s/%s/%s/ws.root '%(indir,sample,mass)
    command += '--rMin=0.001 --rMax=20. '
    command += '--saveToys --saveHybridResult -T %s --clsAcc 0 -s -1 '%(ntoys)
    command += '-n ".azh_%s_%s" '%(sample,proc)
    command += '-m %s '%(mass)
    if batch:
        taskname='limit_%s_%s_%s'%(sample,proc,mass);
        command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s '%(taskname)
    print(command)
    command += ' ; cd %s'%(utils.BaseFolder)

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-sample','--sample',dest='sample',required=True,choices=['2016','2017','2018','Run2','et','mt','tt','em'])
    parser.add_argument('-outdir','--outdir',dest='outdir',required=True,help="""output folder where results of limits are stored""")
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses_ext)
    parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
    parser.add_argument('-strength','--strength',dest='strength',default='0.5')
    parser.add_argument('-ntoys','--ntoys',dest='ntoys',default='200')
    parser.add_argument('-njobs','--njobs',dest='njobs',type=int,default=25)
    parser.add_argument('-folder','--folder',dest='folder',default='datacards',help="""input folder twith datacards""")
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    sample = args.sample
    outdir = args.outdir
    folder = args.folder + '_' + args.proc
    proc = args.proc
    strength = args.strength
    ntoys = args.ntoys
    njobs = args.njobs

    if not args.batch:
        njobs = 1
    
    DatacardsFolder = utils.BaseFolder + '/' + folder

    batch = False
    if args.batch:
        batch = True

    masses = []
    if args.mass=='all':
        masses = utils.azh_masses
    else:
        if args.mass not in utils.azh_masses:
            print('mass %s is not present in the list for azh analysis'%(args.mass))
            exit(1)
        masses.append(args.mass)

 
    fullpath_in = DatacardsFolder+'/'+sample
    if not os.path.isdir(fullpath_in):
        print('')
        print(fullpath_in)
        print('this folder with workspaces does not exist')
        print('first create datacards and workspaces')
        print('')
        exit(1)

    fullpath_out=utils.BaseFolder+'/'+outdir
    if not os.path.isdir(fullpath_out):
        print ('creating folder %s'%(fullpath_out))
        command  = 'mkdir %s'%(fullpath_out)
        os.system(command)

    print('')
    print('Running limits in folder -> ')
    print('%s'%(fullpath_out))
    print('')

    for mA in masses:
        fullpath_ws=DatacardsFolder+'/'+sample+'/'+mA+'/ws.root'
        if not os.path.isfile(fullpath_ws):
            print('Workspace does not exist : %s'%(fullpath_ws))
            print('First create workspaces with macro CreateWorkspaces.py')
            exit(1)

        for i in range(1,njobs+1):
            print('Running CLs : job=%2i sample=%s  proc=%s  mass=%s'%(i,sample,proc,mA))
            command = MakeCommand(sample=sample,
                                  mass=mA,
                                  folder=folder,
                                  strength=strength,
                                  ntoys=ntoys,
                                  proc=proc,
                                  outdir=outdir,
                                  batch=batch)
            os.system(command)
            print('')

    command='cd '+utils.BaseFolder
    os.system(command)
    
    print('')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('All results are saved in folder -> ')
    print('%s'%(fullpath_out))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('')
