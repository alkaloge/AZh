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
    parser.add_argument('-tanb_min','--tanb_min',dest='tanb_min',default='5.0')
    parser.add_argument('-tanb_max','--tanb_max',dest='tanb_max',default='10.0')
    parser.add_argument('-batch','--batch',dest='batch',action='store_true')
    args = parser.parse_args()

    tanb_min = float(args.tanb_min)
    tanb_max = float(args.tanb_max)
    dtanb = 0.1
    if args.model=='mh125EFT_13':
        dtanb = 0.25
    npoints = int((tanb_max-tanb_min)/dtanb) + 1
    masses = ['225','250','275','300','325','350','375','400']
    target = '%s/src/AZh/combine/models/%s'%(os.getenv('CMSSW_BASE'),args.model)
    if os.path.isdir('%s'%(target)):
        print('Running limits for %s'%(args.model))
    else:
        print('folder %s does not exist'%(target))
        exit()

    for mA in masses:
        for i in range(0,npoints+1):
            tanb = tanb_min + dtanb*i
            tanb_str = '%4.2f'%(tanb)
            print(' ')
            print('Running limits on mA=%s and tanb=%s'%(mA,tanb_str))
            print(' ')
            command = 'cd %s ; '%(target)
            command += 'combineTool.py -M AsymptoticLimits --rAbsAcc 0 --rRelAcc 0.0005 ' 
            command += '--X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 1 '
            command += '--cminDefaultMinimizerTolerance 0.01 '
            command += '--setParameters tanb=%s,mA=%s -m %s -d ws_%s.root -n .mssm_tanb%s '%(tanb_str,mA,mA,mA,tanb_str)
            if args.batch: 
                taskname='MSSM_%s_mA%s_tanb%s'%(args.model,mA,tanb_str);
                command += '--job-mode condor --sub-opts=\'+JobFlavour = "workday"\' --task-name %s ; '%(taskname)
            else:
                command += ' ; '
        
            command += 'cd - '
            os.system(command)
