#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

def MakeCommand(**kwargs):

    indir = utils.DatacardsFolder
    outdir = kwargs.get('outdir','limits')
    analysis = kwargs.get('analysis','azh')
    year = kwargs.get('year','Run2')
    obs = kwargs.get('obs',False)
    proc = kwargs.get('proc','ggA')
    release = kwargs.get('releaseOtherPOI',False)
    mass = kwargs.get('mass','1000')
    batch = kwargs.get('batch',False)

    otherProc = 'bbA'
    if proc=='bbA': otherProc = 'ggA'

    typ='exp'
    if obs: typ='obs'

    fullpath_out = utils.BaseFolder+'/'+outdir
    command = 'cd %s ; '%(fullpath_out)
    command += 'combineTool.py -M AsymptoticLimits ' 
    if analysis=='azh':
        command += '-d %s/%s/%s/ws.root '%(indir,year,mass)
        command += '--setParameters r_bbA=0,r_ggA=0 '
        if release:
            command += '--setParameterRanges r_bbA=-30,30:r_ggA=-30,30 '
        else:
            command += '--setParameterRanges r_%s=-30,30 '%(proc)
            command += '--freezeParameters r_%s '%(otherProc)
        command += '--redefineSignalPOIs r_%s '%(proc) 
    else:
        command += '%s/HIG-18-023/%s/ws.root '%(utils.BaseFolder,mass)
        command += '--rMin=0.001 --rMax=50. '
    command += '--rAbsAcc 0 --rRelAcc 0.0005 --X-rtd MINIMIZER_analytic '
    command += '--cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.01 '
    if not obs:
        command += '--noFitAsimov -t -1 '
    command += '-n ".%s_%s_%s" '%(analysis,year,proc)
    command += '-m %s '%(mass)
    if batch:
        taskname='limit_%s_%s_%s_%s'%(year,proc,mass,typ);
        command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s '%(taskname)
    command += ' ; cd %s'%(utils.BaseFolder)

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh',help=""" analysis : azh (this) or hig18023 (HIG-18-023)""",choices=['azh','hig18023'])
    parser.add_argument('-year','--year',dest='year',required=True,help=""" year : 2016, 2017, 2018 or Run2 """,choices=['2016','2017','2018','Run2'])
    parser.add_argument('-obs','--obs',dest='obs',action='store_true',help=""" compute observed limits """)
    parser.add_argument('-releaseOtherPOI','--releaseOtherPOI',dest='releaseOtherPOI',action='store_true',help=""" release other POI, for example r_bbA when running limits on r_ggA or vice versa""")
    parser.add_argument('-outdir','--outdir',dest='outdir',required=True,help=""" output folder to store results of computation""")
    parser.add_argument('-mass','--mass',dest='mass',type=str,required=True,help=""" tested mass of A boson, if \'all\' is specified, limits are computed for all masses""")
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    procs = ['ggA']

    year = args.year
    outdir = args.outdir
    analysis = args.analysis
    releaseOtherPOI = args.releaseOtherPOI
    obs = args.obs

    batch = False
    if args.batch:
        batch = True

    if analysis=='hig18023' or analysis=='HIG18023':
        if year!='2016':
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('Warning! Year %s is not defined for HIG18-023 analysis'%(year))
            print('Changing year to 2016 ')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')        
            year='2016'
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
        fullpath_in = utils.DatacardsFolder+'/'+year
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
            fullpath_ws=utils.DatacardsFolder+'/'+year+'/'+mA+'/ws.root'
            if not os.path.isfile(fullpath_ws):
                print('Workspace does not exist : %s'%(fullpath_ws))
                print('First create workspaces with macro CreateWorkspaces.py')
                exit(1)
        else:
            fullpath_ws=utils.BaseFolder+'/HIG-18-023/'+mA+'/ws.root'
            if not os.path.isfile(fullpath_ws):
                print('Workspace does not exist : %s'%(fullpath_ws))
                print('Nothing is done for year %s and mass %s'%(year,mass))
                print('First create workspaces for HIG-18-023 analysis with script CombineCards_HIG18023.bash')
                exit(1)
        for proc in procs:
            print('Running limit : year=%s  proc=%s  mass=%s'%(year,proc,mA))
            command = MakeCommand(analysis=analysis,
                                  year=year,
                                  obs=obs,
                                  releaseOtherPOI=releaseOtherPOI,
                                  mass=mA,
                                  proc=proc,
                                  outdir=outdir,
                                  batch=batch)
            os.system(command)
            print
            if batch:
                print('executed for : year=%s  proc=%s  mass=%s  with the command:'%(year,proc,mA))
            else:
                print('submitted to condor for year=%s  proc=%s  mass=%s with the command:'%(year,proc,mA))
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
