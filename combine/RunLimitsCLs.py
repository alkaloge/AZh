#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

def MakeCommand(**kwargs):

    outdir = kwargs.get('outdir','limits')
    analysis = kwargs.get('analysis','azh')
    sample = kwargs.get('sample','Run2')
    proc = kwargs.get('proc','ggA')
    mass = kwargs.get('mass','1000')
    batch = kwargs.get('batch',False)
    folder = kwargs.get('folder','datacards')
    strength = kwargs.get('strength','0.5')
    ntoys = kwargs.get('ntoys','100')
    indir = utils.BaseFolder + '/' + folder

    typ='exp'
    if obs: typ='obs'

    fullpath_out = utils.BaseFolder+'/'+outdir
    command = 'cd %s ; '%(fullpath_out)
    command += 'combineTool.py -M HybridNew --LHCmode LHC-limits ' 
    command += '--singlePoint %s '%(strength)
    if analysis=='azh':
        command += '-d %s/%s/%s/ws.root '%(indir,sample,mass)
        command += '--rMin=0.001 --rMax=20. '
    else:
        command += '%s/HIG-18-023/%s/ws.root '%(utils.BaseFolder,mass)
        command += '--rMin=0.001 --rMax=50. '
    command += '--saveToys --saveHybridResult -T %s --clsAcc 0 -s -1 '%(ntoys)
    command += '-n ".%s_%s_%s" '%(analysis,sample,proc)
    command += '-m %s '%(mass)
    if batch:
        taskname='limit_%s_%s_%s_%s'%(sample,proc,mass,typ);
        command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s '%(taskname)
    print(command)
    command += ' ; cd %s'%(utils.BaseFolder)

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh',help=""" analysis : azh (this) or hig18023 (HIG-18-023)""",choices=['azh','hig18023'])
    parser.add_argument('-sample','--sample',dest='sample',required=True,choices=['2016','2017','2018','Run2','et','mt','tt','em'])
    parser.add_argument('-outdir','--outdir',dest='outdir',required=True,help=""" output folder where results of limits are stored""")
    parser.add_argument('-mass','--mass',dest='mass',required=True,choices=utils.azh_masses_ext)
    parser.add_argument('-proc','--proc',dest='proc',required=True,choices=['ggA','bbA'])
    parser.add_argument('-strength','--strength',dest='strength',default='0.5')
    parser.add_argument('-ntoys','--ntoys',dest='ntoys',default='100')
    parser.add_argument('-njobs','--njobs',dest='njobs',type=int,default=10)
    parser.add_argument('-folder','--folder',dest='folder',required=True,help=""" input folder twith datacards""")
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    sample = args.sample
    outdir = args.outdir
    folder = args.folder + '_' + args.proc
    analysis = args.analysis
    proc = args.proc
    strength = args.strength
    ntoys = args.ntoys
    njobs = args.njobs

    DatacardsFolder = utils.BaseFolder + '/' + folder

    batch = False
    if args.batch:
        batch = True

    if analysis=='hig18023' or analysis=='HIG18023':
        if sample!='2016':
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Warning! Year %s is not defined for HIG18-023 analysis'%(sample))
            print('Changing year to 2016 ')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')        
            sample='2016'
        
    masses = []
    if args.mass=='all':
        masses = utils.azh_masses
        if analysis=='hig18023':
            masses = utils.hig18023_masses
    else:
        if analysis=='azh':
            if args.mass not in utils.azh_masses:
                print('mass %s is not present in the list for azh analysis'%(args.mass))
                exit(1)
        else:
            if args.mass not in utils.hig18023_masses:
                print('mass %s is not present in the list for hig18-023 analysis'%(args.mass))
                exit(1)
        masses.append(args.mass)

 
    if analysis=='azh':
        fullpath_in = DatacardsFolder+'/'+sample
        if not os.path.isdir(fullpath_in):
            print
            print(fullpath_in)
            print('this folder with workspaces does not exist')
            print('first create datacards and workspaces')
            print
            exit(1)
    else:
        fullpath_in = utils.BaseFolder+'/HIG-18-023'
        if not os.path.isdir(fullpath_in):
            print
            print(fullpath_in)
            print('this folder with workspaces does not exist')
            print('first setup datacards and workspaces for analysis HIG-18-023')
            print
            exit(1)
            
    

    fullpath_out=utils.BaseFolder+'/'+outdir
    if not os.path.isdir(fullpath_out):
        print ('creating folder %s'%(fullpath_out))
        command  = 'mkdir %s'%(fullpath_out)
        os.system(command)

    print
    print('Running limits in folder -> ')
    print('%s'%(fullpath_out))
    print

    for mA in masses:
        if analysis=='azh':
            fullpath_ws=DatacardsFolder+'/'+sample+'/'+mA+'/ws.root'
            if not os.path.isfile(fullpath_ws):
                print('Workspace does not exist : %s'%(fullpath_ws))
                print('First create workspaces with macro CreateWorkspaces.py')
                exit(1)
        else:
            fullpath_ws=utils.BaseFolder+'/HIG-18-023/'+mA+'/ws.root'
            if not os.path.isfile(fullpath_ws):
                print('Workspace does not exist : %s'%(fullpath_ws))
                print('Nothing is done for sample %s and mass %s'%(sample,mass))
                print('First create workspaces for HIG-18-023 analysis with script CombineCards_HIG18023.bash')
                exit(1)

        for i in range(0,njobs):
            print('Running CLs : job=%2i sample=%s  proc=%s  mass=%s'%(i,sample,proc,mA))
            command = MakeCommand(analysis=analysis,
                                  sample=sample,
                                  mass=mA,
                                  folder=folder,
                                  strength=strength,
                                  ntoys=ntoys,
                                  proc=proc,
                                  outdir=outdir,
                                  batch=batch)
            os.system(command)
            print
            if batch:
                print('submitted to condor for sample=%s  proc=%s  mass=%s with the command:'%(sample,proc,mA))
            else:
                print('executed for : sample=%s  proc=%s  mass=%s  with the command:'%(sample,proc,mA))
            print(command)
            print('')

    command='cd '+utils.BaseFolder
    os.system(command)
    
    print
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('All results are saved in folder -> ')
    print('%s'%(fullpath_out))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print
