#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

def MakeCommand(**kwargs):

    outdir = kwargs.get('outdir','limits')
    analysis = kwargs.get('analysis','azh')
    sample = kwargs.get('sample','Run2')
    obs = kwargs.get('obs',False)
    proc = kwargs.get('proc','ggA')
    release = kwargs.get('releaseOtherPOI',False)
    mass = kwargs.get('mass','1000')
    batch = kwargs.get('batch',False)
    folder = kwargs.get('folder','datacards')
    indir = utils.BaseFolder + '/' + folder

    otherProc = 'bbA'
    if proc=='bbA': otherProc = 'ggA'

    typ='exp'
    if obs: typ='obs'

    fullpath_out = utils.BaseFolder+'/'+outdir
    command = 'cd %s ; '%(fullpath_out)
    command += 'combineTool.py -M AsymptoticLimits ' 
    if analysis=='azh':
        command += '-d %s/%s/%s/ws.root '%(indir,sample,mass)
        command += '--setParameters r_bbA=0,r_ggA=0 '
        if release:
            command += '--setParameterRanges r_%s=0,20:r_%s=0,20 '%(proc,otherProc)
        else:
            command += '--setParameterRanges r_%s=0,20 '%(proc)
            command += '--freezeParameters r_%s '%(otherProc)
        command += '--redefineSignalPOIs r_%s '%(proc) 
    else:
        command += '%s/HIG-18-023/%s/ws.root '%(utils.BaseFolder,mass)
        command += '--rMin=0.001 --rMax=50. '
    command += '--rAbsAcc 0 --rRelAcc 0.0005 '
    command += '--X-rtd MINIMIZER_analytic '
    command += '--cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.01 '
    if not obs:
        command +='-t -1 --noFitAsimov '
    else: 
        if release:
            command +='--noFitAsimov '
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
    parser.add_argument('-sample','--sample',dest='sample',required=True,choices=['2016','2017','2018','Run2','et','mt','tt','em','0btag','btag'])
    parser.add_argument('-outdir','--outdir',dest='outdir',required=True,help=""" output folder where results of limits are stored""")
    parser.add_argument('-mass','--mass',dest='mass',type=str,required=True,help=""" tested mass of A boson, if \'all\' is specified, limits are computed for all masses""")
    parser.add_argument('-obs','--obs',dest='obs',action='store_true',help=""" compute observed limits """)
    parser.add_argument('-releaseOtherPOI','--releaseOtherPOI',dest='releaseOtherPOI',action='store_true',help=""" release other POI, for example r_bbA when running limits on r_ggA or vice versa""")
    parser.add_argument('-folder','--folder',dest='folder',default="datacards",help=""" input folder twith datacards""")
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    procs = ['ggA']

    sample = args.sample
    outdir = args.outdir
    folder = args.folder
    analysis = args.analysis
    releaseOtherPOI = args.releaseOtherPOI
    obs = args.obs

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
    else:
        procs.append('bbA')
        
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
        for proc in procs:
            print('Running limit : sample=%s  proc=%s  mass=%s'%(sample,proc,mA))
            command = MakeCommand(analysis=analysis,
                                  sample=sample,
                                  obs=obs,
                                  releaseOtherPOI=releaseOtherPOI,
                                  mass=mA,
                                  folder=folder,
                                  proc=proc,
                                  outdir=outdir,
                                  batch=batch)
            os.system(command)
            print
            if batch:
                print('executed for : sample=%s  proc=%s  mass=%s  with the command:'%(sample,proc,mA))
            else:
                print('submitted to condor for sample=%s  proc=%s  mass=%s with the command:'%(sample,proc,mA))
            print(command)
            print

    command='cd '+utils.BaseFolder
    os.system(command)
    
    print
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('All results are saved in folder -> ')
    print('%s'%(fullpath_out))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print
