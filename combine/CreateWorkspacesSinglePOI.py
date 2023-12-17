#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

if __name__ == "__main__":

    mass_ext = utils.azh_masses
    mass_ext.append('all')

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-mass','--mass',dest='mass',default='1000')
    parser.add_argument('-proc','--proc',dest='proc',default='ggA')
    args = parser.parse_args()

    years = utils.years
    cats = utils.azh_cats
    proc = args.proc
    outdir = 'datacards'
    mass = args.mass
    procs = utils.azh_signals

    if not proc in procs:
        print('Uknown process : %s'%(proc))
        print('available options : "bbA" and "ggA"')
        exit(1)


    for year in years:
        print
        print('Creating datacards for single process %s%s'%(proc,mass))
        print
        for cat in cats:
            print('Creating cards : %s -- category : %s -- mass : %s'%(year,cat,mass))
            command = './make_datacards.py --year %s --btag %s --mass %s --proc %s'%(year,cat,mass,proc)
            os.system(command)
        command = 'combineTool.py -M T2W -o "ws.root" -i %s_%s/%s/%s -m %s'%(outdir,proc,year,mass,mass)
        os.system(command)

    command = 'combineTool.py -M T2W -o "ws.root" -i %s_%s/Run2/%s -m %s'%(outdir,proc,mass,mass)
    os.system(command)

    print
    print('datacards and workspaces with single process %s are written to folder "%s_%s"'%(proc,outdir,proc))
    print
