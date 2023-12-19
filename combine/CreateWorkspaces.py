#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

def MakeCommandWorkspace(**kwargs):
    proc = kwargs.get('proc','2poi')
    year = kwargs.get('year','Run2')
    mass = kwargs.get('mass','1000')
    outdir = kwargs.get('outdir','datacards')
    command = 'combineTool.py -M T2W -o "ws.root" -i %s_%s/%s/%s -m %s'%(outdir,proc,year,mass,mass)
    if proc=='2poi':
        command = 'combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/bbA$:r_bbA[0,-40,40]"\' --PO \'"map=^.*/ggA$:r_ggA[0,-40,40]"\' -i datacards/%s/%s -m %s'%(year,mass,mass)

    return command

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-year','--year',dest='year',default='Run2',help=""" year : 2016 2017 2018 Run2""",choices=utils.years_ext)
    parser.add_argument('-mass','--mass',dest='mass',default='1000',help=""" single mA point, if \'all\' is given as an argument, then workspaces for all masses will be created""",choices=utils.azh_masses_ext)
    parser.add_argument('-proc','--proc',dest='proc',default='2poi',help=""" proc : ggA, bbA or 2poi """,choices=['ggA','bbA','2poi'])
    args = parser.parse_args()

    proc = args.proc
    outdir = utils.DatacardsFolder+'_'+proc
    if proc=='2poi':
        outdir = utils.DatacardsFolder
    year = args.year
    masses = []
    if args.mass=='all':
        masses = utils.azh_masses
    else:
        masses.append(args.mass)


    folder = utils.BaseFolder+'/'+outdir+'/'+year
    if not os.path.isdir(folder):
        print ('Folder %s does not exist'%(folder))
        print ('Run first datacard production with script make_datacards.py or CreateCards.py')
        exit(1)

    for mA in masses:
        print
        folder_mass = utils.BaseFolder+'/'+outdir+'/'+year+'/'+mA
        if not os.path.isdir(folder_mass):
            print('Folder %s does not exist'%(folder_mass))
            print ('Run first datacard production with script make_datacards.py or CreateCards.py')
            exit(1)

        ws_file=folder_mass+'/ws.root'
        if os.path.isfile(ws_file):
            rm_command = 'rm '+ws_file
            print('file exist %s'%(ws_file))
            print(rm_command)
            os.system(rm_command)

        datacard_file=folder_mass+'/combined.txt.cmb'
        if os.path.isfile(datacard_file):
            rm_command = 'rm '+datacard_file
            print('file exist %s'%(datacard_file))
            print(rm_command)
            os.system(rm_command)

        print("Creating workspace in folder %s/%s/%s"%(outdir,year,mA))
            
        command=MakeCommandWorkspace(proc=proc,year=year,mass=mA)
        print(command)
        os.system(command)
