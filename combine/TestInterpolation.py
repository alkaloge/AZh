#! /usr/bin/env python

import ROOT
from array import array

### interpolation between adjacent bin centers
### first argument - real variable
### second argument - histogram
def interpolateHisto(x,hist):
    y,e = 1,0.1
    nbins = hist.GetNbinsX()
    if x<hist.GetBinCenter(1):
        return hist.GetBinContent(1),hist.GetBinError(1)
    if x>hist.GetBinCenter(nbins):
        return hist.GetBinContent(nbins),hist.GetBinError(nbins)
    for ib in range(1,nbins):
        x1 = hist.GetBinCenter(ib)
        x2 = hist.GetBinCenter(ib+1)
        if x>x1 and x<x2:
            y1 = hist.GetBinContent(ib)
            y2 = hist.GetBinContent(ib+1)
            e1 = hist.GetBinError(ib)
            e2 = hist.GetBinContent(ib+1)
            dx = x2 - x1
            dy = y2 - y1
            de = e2 - e1
            y = y1 + (x-x1)*dy/dx
            e = e1 + (x-x1)*de/dx
            return y,e
    return y,e


##########################
#### Testing code ########
##########################
if __name__ == "__main__":

    ROOT.gROOT.SetBatch(True)

    nbins = 6
    bins  = [0.0, 1.0, 2.0, 4.0, 5.0, 8.0, 10.0]
    xbins = [4.0, 2.2, 6.1, 1.6, 5.2, 7.2]
    ebins = [0.0, 0.1, 0.14, 0.2, 0.3, 0.4]
    hist = ROOT.TH1D("h1","",nbins,array('d',list(bins)))
    test_hist = ROOT.TH1D('test_hist','',100,0,10)

    for ib in range(0,nbins):
        hist.SetBinContent(ib+1,xbins[ib])
        hist.SetBinError(ib+1,ebins[ib])

    for ib in range(1,1000):
        x = 0.01*ib
        y,e = interpolateHisto(x,hist)
        test_hist.SetBinContent(test_hist.FindBin(x),y)        
        #        test_hist.SetBinError(test_hist.FindBin(x),e)
        # print(x,y)

    hist.GetYaxis().SetRangeUser(0.,10.)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1.5)
    hist.SetLineWidth(2)

    test_hist.SetLineColor(2)
    test_hist.SetLineWidth(2)

    canv = ROOT.TCanvas('canv','',600,600)
    hist.Draw('e1')
    test_hist.Draw('lsame')
    canv.Update()
    canv.Print('lin_interp.png')
