#!/usr/bin/env python

import CombineHarvester.CombineTools.plotting as plot 
import ROOT
import math
import argparse
from array import array

print('PIDARY 0')


parser = argparse.ArgumentParser()
parser.add_argument(
    '--output', '-o', default='limit', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--mass', default='', help="""Mass label on the plot""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--x-title', default='#kappa_{t}', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='#kappa_{b}', help="""Title for the x-axis""")
parser.add_argument(
    '--debug-output', '-d', help="""If specified, write the contour TH2s and
    TGraphs into this output ROOT file""")
args = parser.parse_args()

print('PIDARY 1')


print('PIDARY 2')

files = ['Scan.root']

#Create canvas and TH2D for each component
#plot.ModTDRStyle(width=600, l=0.12)
print('PIDARY 3')

ROOT.gStyle.SetNdivisions(510, 'XYZ')
plot.SetBirdPalette()
print('PIDARY 1')
canv = ROOT.TCanvas(args.output, args.output)
print('PIDARY 1')
pads = plot.OnePad()


if args.debug_output is not None:
    debug = ROOT.TFile(args.debug_output, 'RECREATE')
else:
    debug = None

print('PIDARY 2')

name = args.files[0].split("/")[-2]
limit = plot.MakeTChain(args.files, 'limit')

print('PIDARY 3')




graph = plot.TGraph2DFromTree(
    limit, var1, var2, '2*deltaNLL', 'quantileExpected > -0.5 && deltaNLL > 0 && deltaNLL < 10')
best = plot.TGraphFromTree(
    limit, var1, var2, 'deltaNLL == 0')
plot.RemoveGraphXDuplicates(best)
hists = plot.TH2FromTGraph2D(graph, method='BinCenterAligned')
plot.fastFillTH2(hists, graph,interpolateMissing=True)

hists.SetMaximum(6)
hists.SetMinimum(0)
hists.SetContour(255)
# c2=ROOT.TCanvas()
# hists.Draw("COLZ")
# c2.SaveAs("heatmap.png")

axis = ROOT.TH2D(hists.GetName(),hists.GetName(),hists.GetXaxis().GetNbins(),hists.GetXaxis().GetXmin(),hists.GetXaxis().GetXmax(),hists.GetYaxis().GetNbins(),hists.GetYaxis().GetXmin(),hists.GetYaxis().GetXmax())
axis.Reset()
axis.GetXaxis().SetTitle(args.x_title)
axis.GetXaxis().SetLabelSize(0.025)
axis.GetYaxis().SetLabelSize(0.025)
axis.GetYaxis().SetTitle(args.y_title)

cont_1sigma = plot.contourFromTH2(hists, ROOT.Math.chisquared_quantile_c(1 - 0.68, 2), 10, frameValue=20)
cont_2sigma = plot.contourFromTH2(hists, ROOT.Math.chisquared_quantile_c(1 - 0.95, 2), 10, frameValue=20)

if debug is not None:
    debug.WriteTObject(hists, 'hist')
    for i, cont in enumerate(cont_1sigma):
        debug.WriteTObject(cont, 'cont_1sigma_%i' % i)
    for i, cont in enumerate(cont_2sigma):
        debug.WriteTObject(cont, 'cont_2sigma_%i' % i)

if args.sm_exp or args.bg_exp:
    legend = plot.PositionedLegend(0.3, 0.25, 3, 0.015)
else:
    legend = plot.PositionedLegend(0.15, 0.2, 3, 0.015)

pads[0].cd()
axis.Draw()
for i, p in enumerate(cont_2sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-10)
    p.SetFillStyle(1001)
    p.Draw("F SAME")
    p.Draw("L SAME")
legend.AddEntry(cont_2sigma[0], "95% CL", "F")

for i, p in enumerate(cont_1sigma):
    p.SetLineStyle(1)
    p.SetLineWidth(2)
    p.SetLineColor(ROOT.kBlack)
    p.SetFillColor(ROOT.kBlue-8)
    p.SetFillStyle(1001)
    p.Draw("F SAME")
    p.Draw("L SAME")
legend.AddEntry(cont_1sigma[0], "68% CL", "F")

best.SetMarkerStyle(34)
best.SetMarkerSize(3)
best.Draw("P SAME")
legend.AddEntry(best, "Best fit", "P")
if args.sm_exp:
    best_sm.SetMarkerStyle(33)
    best_sm.SetMarkerColor(1)
    best_sm.SetMarkerSize(3.0)
    best_sm.Draw("P SAME")
    legend.AddEntry(best_sm, "Expected for 125 GeV SM Higgs", "P")
if args.bg_exp:
    best_bg.SetMarkerStyle(33)
    best_bg.SetMarkerColor(46)
    best_bg.SetMarkerSize(3)
    best_bg.Draw("P SAME")
    legend.AddEntry(best_bg, "Expected for background only", "P")


if args.mass:
    legend.SetHeader("m_{#phi} = "+args.mass+" GeV")
legend.Draw("SAME")
if args.sm_exp:
    overlayLegend,overlayGraphs = plot.getOverlayMarkerAndLegend(legend, {legend.GetNRows()-1 : best_sm}, {legend.GetNRows()-1 : {"MarkerColor" : 2}}, markerStyle="P")

plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.035, 1.2, '', 1.0)
plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawTitle(pads[0], args.title_left, 1)
plot.FixOverlay()
if args.sm_exp:
    best_sm.Draw("P SAME")
    for overlayGraph in overlayGraphs:
        print "test"
        overlayGraph.Draw("P SAME")
    overlayLegend.Draw("SAME")
canv.Print('figures/'+name+'.pdf')
canv.Print('figures/'+name+'.png')
canv.Close()

if debug is not None:
    debug.Close()
