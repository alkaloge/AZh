#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-year','--year',dest='year',default='Run2')
    args = parser.parse_args()

    outdir = 'datacards'
    year = args.year
    masses = utils.azh_masses

    folder = utils.BaseFolder+'/'+outdir+'/'+year
    if not os.path.isdir(folder):
        print ('Folder %s does not exist'%(folder))
        print ('Run first datacards with the following parameters :')
        print ('./make_datacards.py --year {2016,2017,2018} --outdir %s'%(outdir))
        exit(1)

    for mA in masses:
        print
        print("Creating workspace in folder %s/%s/%s"%(outdir,year,mA))
        command=utils.BaseFolder+'/CreateWorkspace.bash %s %s %s'%(year,mA,outdir)
        print
        #os.system(command)
        print
        print
