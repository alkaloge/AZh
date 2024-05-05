#!/usr/bin/env python
import os
from collections import defaultdict
import math
import json

import numpy as np

import ROOT

from HiggsAnalysis.CombinedLimit.PhysicsModel import *


class AZhModel(PhysicsModel):

    def __init__(self):
        PhysicsModel.__init__(self)
        # Add containers to store set of defined signal processes,
        # the associated systematic uncertainties and nuisance parameters
        self.PROC_SETS = []
        self.SYST_DICT = defaultdict(list)
        self.NUISANCES = set()
        self.scenario = 'hMSSM_13'
        self.tanbeta = 2.0
        self.mA = 300.0
        self.debug_output = None

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith('Scenario='):
                self.scenario = po.replace('Scenario=', '')
                print 'Scenario : %s' % self.scenario
            if po.startswith('tanb='):
                self.tanbeta = float(po.replace('tanb=',''))
            if po.startswith('mA='):
                self.mA = float(po.replace('mA=',''))
        if self.scenario not in ['hMSSM_13','mh125EFT_13']:
            print('unknown scenario: %s'%(self.scenario))

        self.filename = os.getenv("CMSSW_BASE")+'/src/AZh/combine/models/'+self.scenario+'.root'

    def setModelBuilder(self, modelBuilder):
        """Used to load quantities in empty workspace."""
        # First call the parent class implementation
        PhysicsModel.setModelBuilder(self,modelBuilder)
        # Function to implement the histograms of (mA, tanb) dependent quantities
        self.buildModel()

    def buildModel(self):
        mass = ROOT.RooRealVar('mA', 'm_{A} [GeV]', self.mA)
        tanb = ROOT.RooRealVar('tanb', 'tan#beta',self.tanbeta)
        pars = [mass, tanb]

        print('Building model : mA = %4.0f  tanbeta=%4.1f'%(mass.getVal(),tanb.getVal()))

        # Open input root file to read the histograms
        rf = ROOT.TFile(self.filename, "read")

        self.doHistFunc("br_AZh",rf.Get("br_A_Zh"), pars)
        self.doHistFunc("br_htautau",rf.Get("br_h_tautau"), pars)
        self.doHistFunc("xs_ggA",rf.Get("xs_gg_A"), pars)
        self.doHistFunc("xs_bbA",rf.Get("xs_bb_A"), pars)

        # ggH scale uncertainty
        self.doAsymPowSystematic("A", "xs", pars, "gg", "scale")
        # ggH pdf+alpha_s uncertainty
        self.doAsymPowSystematic("A", "xs", pars, "gg", "pdfas")
        # bbH total uncertainty 
        self.doAsymPowSystematic("A", "xs", pars, "bb", "")

        self.SYST_DICT['xs_ggA'].append('systeff_xs_ggA_scale')
        self.SYST_DICT['xs_ggA'].append('systeff_xs_ggA_pdfas')
        self.SYST_DICT['xs_bbA'].append('systeff_xs_bbA_total')

        # Make a note of what we've built, will be used to create scaling expressions later
        self.PROC_SETS.append('ggA')
        self.PROC_SETS.append('bbA')

        if self.debug_output:
            self.debug_output.Close()
        return

    def preProcessNuisances(self,nuisances):
        doParams = set()
        for bin in self.DC.bins:
            for proc in self.DC.exp[bin].keys():
                if self.DC.isSignal[proc]:
                    scaling = 'scaling_%s' % proc
                    #                    print(scaling)
                    params = self.modelBuilder.out.function(scaling).getParameters(ROOT.RooArgSet()).contentsString().split(',')
                    for param in params:
                        if param in self.NUISANCES:
                            doParams.add(param)
        for param in doParams:
            print 'Add nuisance parameter %s to datacard' % param
            nuisances.append((param,False, "param", [ "0", "1"], [] ) )

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("r[1,0,20]")
        self.modelBuilder.doSet('POI', 'r')

        # We don't intend on actually floating these in any fits...
        self.modelBuilder.out.var('mA').setConstant(True)
        self.modelBuilder.out.var('tanb').setConstant(True)
        #        self.modelBuilder.out.var('br_Zll').setConstant(True)

        for proc in self.PROC_SETS:
            # Set up list of terms used in the scaling of the considered process
            terms = ['xs_%s' % proc,'br_AZh','br_htautau','100.0','r']
            # Check if a term was added that is associated with
            # a systematic uncertainty. If this is the case add
            # the systematic uncertainty to the scaling of the process
            #            extra = []
            #            for term in terms:
            #                if term in self.SYST_DICT:
            #            extra += self.SYST_DICT[term]
            #            terms.extend(extra)
            print(proc, terms)
            # Add scaling function for the process to the workspace
            print('prod::scaling_%s(%s)'%(proc,','.join(terms)))
            self.modelBuilder.factory_('prod::scaling_%s(%s)'%(proc,','.join(terms)))
            self.modelBuilder.out.function('scaling_%s'%proc).Print('')

    def doAsymPowSystematic(self, higgs, quantity, varlist, production, uncertainty):
        # create AsymPow rate scaler given two TH2 inputs corresponding to kappa_hi and kappa_lo
        nameHist = "{q}_{pr}_{h}".format(q=quantity, pr=production, h=higgs)
        name = "{q}_{pr}{h}".format(q=quantity, pr=production, h=higgs)
        param = name + '_' + uncertainty
        if uncertainty=='':
            param = name + '_total'
        self.modelBuilder.doVar('%s[0,-7,7]'%param)
        param_var = self.modelBuilder.out.var(param)
        systname = "systeff_%s"%param

        # Open input root file to read the histograms
        # print(self.filename,nameHist)
        rf = ROOT.TFile(self.filename, "read")
        hist_hi = rf.Get("{nameHist}_{unc}up".format(nameHist=nameHist, unc=uncertainty))
        hist_lo = rf.Get("{nameHist}_{unc}down".format(nameHist=nameHist, unc=uncertainty))
        # Currently the histograms in stored in the root file only represent
        # the value of the uncertainty. For a meaningful result the
        # prediction for the quantity needs to be added.
        hist_nom = rf.Get(nameHist)
        nbinsx = hist_nom.GetNbinsX()
        nbinsy = hist_nom.GetNbinsY()
        for i in range(1,nbinsx+1):
            for j in range(nbinsy+1):
                nom = max(hist_nom.GetBinContent(i,j),0.0001)
                hi = 1.0+hist_hi.GetBinContent(i,j)/nom
                lo = 1.0+hist_lo.GetBinContent(i,j)/nom
                hist_hi.SetBinContent(i,j,hi)
                hist_lo.SetBinContent(i,j,lo)

        self.NUISANCES.add(param)
        hi = self.doHistFunc('%s_hi'%systname, hist_hi, varlist)
        lo = self.doHistFunc('%s_lo'%systname, hist_lo, varlist)
        asym = ROOT.AsymPow(systname, '', lo, hi, param_var)
        self.modelBuilder.out._import(asym)
        return self.modelBuilder.out.function(systname)

    def getYieldScale(self,bin,process):
        if self.DC.isSignal[process]:
            scaling = 'scaling_%s'%process
            print 'Scaling %s/%s as %s' % (bin, process, scaling)
            return scaling
        else:
            return 1

    def doHistFunc(self, name, hist, varlist):
        if self.debug_output:
            self.debug_output.cd()
            hist.Write()
        dh = ROOT.RooDataHist('dh_%s'%name, 'dh_%s'%name, ROOT.RooArgList(*varlist), ROOT.RooFit.Import(hist))
        hfunc = ROOT.RooHistFunc(name, name, ROOT.RooArgSet(*varlist), dh)
        self.modelBuilder.out._import(hfunc, ROOT.RooFit.RecycleConflictNodes())
        return self.modelBuilder.out.function(name)

AZhModel = AZhModel()
