#!/usr/bin/env python

import AZh.combine.utilsAZh as utils
import os

if __name__ == "__main__":

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument()
    parser.add_argument('-analysis','--analysis',dest='analysis',default='azh')
    parser.add_argument('-proc','--proc',dest='proc',default='ggA')
    parser.add_argument('-mass','--mass',dest='mass',default='1000')
    parser.add_argument('-type','--type',dest='typeImpacts',default='exp')
    args = parser.parse_args()
    
    if analysis not in  

    Expect = False
    prefix = 'obs'
    proc = args.proc
    mass = args.mass
    if args.typeImpacts in 'expected' or args.typeImpacts in 'Expected':
        Expect = True
        prefix = 'exp'

    if ()

    pathdir = utils.BaseFolder + '/' + prefix + '_impacts_'+analysis+'_'




