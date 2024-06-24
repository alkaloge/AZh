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
        command = 'mkdir %s ; cp %s.root %s '%(target)
        os.system(command)
#    else:
#        print('Cleaning folder %s'%(target))
#        command = 'cd %s ; rm * ; cd - '
#        os.system(command)

    command = 'cd %s ; '%(target) 
    if not os.path.isdir(target):
        exit()

#    masses = ['225','250','275','300','325','350','375','400']
    masses = ['225']
    for mass in masses:
        command = 'cd %s ; '%(target)
        command += 'rm combined.txt.cmb ; rm azh* ; '
        command += 'cp %s/src/AZh/combine/models/%s.root ./ ;'%(os.getenv('CMSSW_BASE'),args.model)
        command += 'cp %s/src/AZh/combine/datacards/Run2/%s/azh* %s/src/AZh/combine/models/%s ; '%(os.getenv('CMSSW_BASE'),mass,os.getenv('CMSSW_BASE'),args.model)
        command += 'combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.AZhModel:AZhModel '
        command += '--PO tanb=1 --PO mA=%s --PO scenario=%s -i %s -o "ws_%s.root" -m %s ; '%(mass,args.model,target,mass,mass)
        command += 'cd - '
        os.system(command)

