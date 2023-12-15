#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

def MakeCommand(**kwargs):

    indir = kwargs.get('indir','datacards')
    outdir = kwargs.get('outdir','limits')
    analysis = kwargs.get('analysis','azh')
    year = kwargs.get('year','Run2')
    expected = kwargs.get('exp',True)
    proc = kwargs.get('proc','ggA')
    freeze = kwargs.get('freeze',True)
    mass = kwargs.get('mass','1000')

    fullpath_out = utils.BaseFolder+'/'+outdir
    
    command = 'cd %s ; '%(fullpath_out)
    command += 'combine -M AsymptoticLimits ' 
    if analysis=='azh' or analysis=='AZh':
        command += '-d %s/%s/%s/%s/ws.root '%(utils.BaseFolder,indir,year,mass)
        command += '--setParameters r_bbA=0,r_ggA=0 '
        if freeze:
            command += '--setParameterRanges r_bbA=0,50:r_ggA=0,50 '
        else:
            command += '----setParameterRanges r_bbA=-20,50:r_ggA=-20,50 '
        command += '--redefineSignalPOIs r_%s '%(proc) 
    else:
        command += '%s/HIG-18-023/%s/ws.root '%(utils.BaseFolder,mass)
        command += '--rMin=0.001 --rMax=50. '
    command += '--rAbsAcc 0 --rRelAcc 0.0005 --X-rtd MINIMIZER_analytic '
    command += '--cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.01 '
    if expected:
        command += '--noFitAsimov -t -1 '
    command += '-n ".%s_%s_%s" '%(analysis,year,proc)
    command += '-m %s'%(mass)
    command += ' ; cd %s'%(utils.BaseFolder)

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-year','--year',dest='year',default='Run2')
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh')
    parser.add_argument('-type','--type',dest='typeLimit',default='Exp',help=""" Type of limit : Exp (exp), or Obs(obs)""")
    parser.add_argument('-freezeOtherPOI','--freezeOtherPOI',dest='freeze',default='yes')
    parser.add_argument('-outdir','--outdir',dest='outdir',default='limits')
    parser.add_argument('-mass','--mass',dest='mass',default='1000')
    args = parser.parse_args()

    procs = ['ggA']

    year = args.year
    indir = 'datacards'
    outdir = args.outdir
    analysis = args.analysis

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
        

    Expect = False
    if (args.typeLimit in 'Expected') or (args.typeLimit in 'expected'):
        Expect = True
    
    Freeze = False
    if (args.freeze in 'yes') or (args.freeze in 'Yes'):
        Freeze = True

    masses = []
    if args.mass=='*' or args.mass=='all' or args.mass=='All':
        masses = utils.azh_masses
        if analysis=='hig18023' or analysis=='HIG18023':
            masses = utils.hig18023_masses
    else:
        masses.append(args.mass)
 
    fullpath_in = utils.BaseFolder+'/'+indir
    if not os.path.isdir(fullpath_in):
        print(fullpath_in)
        print('input folder %s does not exist'%(indir))
        exit(1)

    fullpath_out=utils.BaseFolder+'/'+outdir
    if not os.path.isdir(fullpath_out):
        print ('creating folder %s'%(fullpath_out))
        command  = 'mkdir %s'%(fullpath_out)
        os.system(command)

    print
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('Running limits in folder -> ')
    print('%s'%(fullpath_out))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print

    for mA in masses:
        for proc in procs:
            print('Running limit : year=%s  proc=%s  mass=%s'%(year,proc,mA))
            command = MakeCommand(analysis=analysis,indir=indir,year=year,expected=Expect,freeze=Freeze,mass=mA,proc=proc,outdir=outdir)
            os.system(command)
            print
            print('done computation for : year=%s  proc=%s  mass=%s  with the command:'%(year,proc,mA))
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
