#!/usr/bin/env python3

import math

def computeUncChannel(channel,bkg,yields_chan,uncs_chan):
    tot = yields_chan[channel][bkg]
    uncs = uncs_chan[channel]
    totE2 = 0
    for unc in uncs:
        if bkg=='fakes':
            if unc in ['fakes']: totE2 += uncs[unc]*uncs[unc]
        if bkg=='ZZ':
            if unc in ['ZZ','lepID','btag']: totE2 += uncs[unc]*uncs[unc]
        if bkg=='other':
            if unc in ['other','lepID','btag']: totE2 += uncs[unc]*uncs[unc]
            
    totE = tot*math.sqrt(totE2)
    return tot,totE
    

def computeUncTotal(channel,yields_chan,uncs_chan):
    uncs = uncs_chan[channel]
    yields = yields_chan[channel]
    totbkg = 0
    totbkgE2 = 0
    uncorr = {
        'fakes' : 0,
        'ZZ'    : 0,
        'other' : 0,
        'lepID' : 0,
        'btag'  : 0
    }

    for bkg in yields:
        totbkg += yields[bkg]
        if bkg=='fakes': uncorr['fakes'] += yields[bkg]*uncs['fakes']
        if bkg=='ZZ': 
            uncorr['ZZ'] += yields[bkg]*uncs['ZZ']
            uncorr['lepID'] += yields[bkg]*uncs['lepID']
            uncorr['btag'] += yields[bkg]*uncs['btag']
        if bkg=='other':
            uncorr['other'] +=  yields[bkg]*uncs['other']
            uncorr['lepID'] += yields[bkg]*uncs['lepID']
            uncorr['btag'] += yields[bkg]*uncs['btag']

    for err in uncorr:
        totbkgE2 += uncorr[err]*uncorr[err]
    totbkgE = math.sqrt(totbkgE2)

    return totbkg,totbkgE
            

uncs_nobtag = {
    'et' : { 'fakes' : 0.28, 'ZZ' : 0.12, 'other' : 0.23, 'lepID' : 0.05, 'btag' : 0.03},
    'mt' : { 'fakes' : 0.23, 'ZZ' : 0.10, 'other' : 0.22, 'lepID' : 0.04, 'btag' : 0.03},
    'tt' : { 'fakes' : 0.25, 'ZZ' : 0.11, 'other' : 0.21, 'lepID' : 0.04, 'btag' : 0.04}
}

uncs_btag = {
    'et' : { 'fakes' : 0.32, 'ZZ' : 0.12, 'other' : 0.23, 'lepID' : 0.05, 'btag' : 0.12},
    'mt' : { 'fakes' : 0.29, 'ZZ' : 0.10, 'other' : 0.22, 'lepID' : 0.04, 'btag' : 0.13},
    'tt' : { 'fakes' : 0.29, 'ZZ' : 0.11, 'other' : 0.21, 'lepID' : 0.04, 'btag' : 0.12}
}

yields_nobtag = {
    'et' : { 'fakes' : 18.72, 'ZZ' : 25.61, 'other' : 4.44},
    'mt' : { 'fakes' : 14.83, 'ZZ' : 36.41, 'other' : 6.62},
    'tt' : { 'fakes' : 33.47, 'ZZ' : 41.87, 'other' : 6.99},
}

yields_btag = {
    'et' : { 'fakes' : 3.41, 'ZZ' : 0.75, 'other' : 0.99},
    'mt' : { 'fakes' : 1.69, 'ZZ' : 1.09, 'other' : 1.43},
    'tt' : { 'fakes' : 1.21, 'ZZ' : 1.28, 'other' : 0.68}
}

yields_cat = {
    'nobtag' : yields_nobtag,
    'btag' : yields_btag
}

uncs_cat = {
    'nobtag' : uncs_nobtag,
    'btag' : uncs_btag
}

bkgs = ['ZZ', 'fakes', 'other']
chans = ['et', 'mt', 'tt']
cats = ['nobtag','btag']

titles = {
    'ZZ'    : 'ZZ    ',
    'fakes' : 'fakes ',
    'other' : 'other ',
}

for bkg in bkgs:
    x = {}
    ex = {}
    for cat in cats:
        for chan in chans:
            label = '%s_%s'%(cat,chan)
            uncs = uncs_cat[cat]
            yields = yields_cat[cat]
            tot,totE = computeUncChannel(chan,bkg,yields,uncs)
            x[label] = tot
            ex[label] = totE
    line = '%s &'%(titles[bkg])
    for entry in x:
        if 'nobtag' in entry:
            line += ' %5.1f$\pm$%5.1f &'%(x[entry],ex[entry])
        else:
            line += ' %5.2f$\pm$%5.2f &'%(x[entry],ex[entry])
            
    print(line)

xtot = {}
xtotE = {}
for cat in cats:
    for chan in chans:
        label = '%s_%s'%(cat,chan)
        uncs = uncs_cat[cat]
        yields = yields_cat[cat]
        tot,totE = computeUncTotal(chan,yields,uncs)
        xtot[label] = tot
        xtotE[label] = totE

line = 'Total  &'
for entry in xtot:
    if 'nobtag' in entry:
        line += ' %5.1f$\pm$%5.1f &'%(xtot[entry],xtotE[entry])
    else:
        line += ' %5.2f$\pm$%5.2f &'%(xtot[entry],xtotE[entry])
            
print(line)
