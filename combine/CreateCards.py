#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

###### main ############
if __name__ == "__main__":

    years = utils.years
    cats = utils.azh_cats
    masses = utils.azh_masses

    for year in years:
        for cat in cats:
            for mass in masses:
                print('Creating cards : %s -- category : %s -- mass : %s'%(year,cat,mass))
                command = utils.BaseFolder+'/make_datacards.py --year %s --btag %s --mass %s'%(year,cat,mass)
                os.system(command)

    print
    print('++++++++++++++++++++++++++++++++++++++++++++++++')
    print('datacards are written to folder "datacards"     ')
    print('++++++++++++++++++++++++++++++++++++++++++++++++')
