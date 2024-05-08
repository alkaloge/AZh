#!/usr/bin/env python
import os
import math
import numpy as np
import ROOT
import AZh.combine.stylesAZh as styles
import argparse
    

############
### MAIN ###
############
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)
    styles.InitROOT()
    styles.SetStyle()

    
    parser = argparse.ArgumentParser(description="Creates MSSM Model")
    parser.add_argument('-model','--model',dest='model',default='mh125EFT_13',choices=['hMSSM_13','mh125EFT_13'])
    args = parser.parse_args()

    target = '%s/src/AZh/combine/models/%s'%(os.getenv('CMSSW_BASE'),args.model)
    if not os.path.isdir(target):
        print('Creating cards in folder %s'%(target))
        command = 'mkdir %s'%(target)
        os.system(command)
    else:
        print('Cleaning folder %s'%(target))
        command = 'cd %s ; rm * ; cd - '
        os.system(command)

    command = 'cd %s ; '%(target) 
    for mass in masses:
        command += 'rm combined.txt.cmb ; rm azh* ; '
        command += 'cp %s/src/AZh/combine/models/%s.root ./ ;'%(os.getenv('CMSSW_BASE'),args.model)
        command += 'cp %s/src/AZh/combine/datacards/Run2/%s/azh* %s/src/AZh/combine/models/%s ; '%(os.getenv('CMSSW_BASE'),args.mass,os.getenv('CMSSW_BASE'),args.model)

        command += 'combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.AZhModel:AZhModel '
        command += '--PO tanb=1 --PO mA=%s --PO scenario=%s -i %s -o "ws_%s.root" -m %s ; '%(args.mass,args.model,target,args.mass,args.mass)
    command += 'cd - '
    os.system(command)

    for i in range(0,npoints+1):
        tanb = tanb_min + dtanb*i
        tanb_str = '%4.2f'%(tanb)
        print(' ')
        print('Running limits on mA=%s and tanb=%s'%(args.mass,tanb_str))
        print(' ')
        command = 'cd %s ; '%(target)
        command += 'combineTool.py -M AsymptoticLimits --rAbsAcc 0 --rRelAcc 0.0005 ' 
        command += '--X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 1 '
        command += '--cminDefaultMinimizerTolerance 0.01 '
        command += '--setParameters tanb=%s,mA=%s -m %s -d ws_%s.root -n .mssm_tanb%s '%(tanb_str,args.mass,args.mass,args.mass,tanb_str)
        if args.batch: 
            taskname='MSSM_%s_mA%s_tanb%s'%(args.model,args.mass,tanb_str);
            command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s ; '%(taskname)
        else:
            command += ' ; '
        
        command += 'cd - '
        os.system(command)
