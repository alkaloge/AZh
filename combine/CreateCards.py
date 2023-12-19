#!/usr/bin/env python

import os
import AZh.combine.utilsAZh as utils

###### main ############
if __name__ == "__main__":

    years = utils.years
    cats = utils.azh_cats
    masses = utils.azh_masses
    procs = utils.azh_signals

    for year in years:
        for mass in masses:
            for cat in cats:
                command = 'make_datacards.py --year %s --proc 2poi --btag %s --mass %s'%(year,cat,mass)      
                full_command = utils.BaseFolder+'/'+command
                print(command)
                os.system(full_command)
                for proc in procs:
                    command = 'make_datacards.py --year %s --btag %s --proc %s --mass %s'%(year,cat,proc,mass)
                    full_command = utils.BaseFolder+'/'+command
                    print(command)
                    os.system(full_command)

    print
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('datacards with 2 POIs are written to folder "datacards"              ')
    print('datacards with single POI r_ggA are written to folder "datacards_ggA"')
    print('datacards with single POI r_bbA are written to folder "datacards_bbA"')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
