#!/usr/bin/env python

import argparse
import os
import math

import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch
import uproot
import ROOT

cats_all = [
    (1, "eeem"),
    (2, "eeet"),
    (3, "eemt"),
    (4, "eett"),
    (5, "mmem"),
    (6, "mmet"),
    (7, "mmmt"),
    (8, "mmtt"),
]

cats_noem = [
    (1, "eeet"),
    (2, "eemt"),
    (3, "eett"),
    (4, "mmet"),
    (5, "mmmt"),
    (6, "mmtt"),
]

cats_em = [
    (1, "eeem"),
    (2, "mmem")
]

cats_et = [
    (1, "eeet"),
    (2, "mmet")
]

cats_mt = [
    (1, "eemt"),
    (2, "mmmt")
]

cats_tt = [
    (1, "eett"),
    (2, "mmtt")
]

cats_ditau = {
    'em' : cats_em,
    'et' : cats_et,
    'mt' : cats_mt,
    'tt' : cats_tt
}

#############################################
# uncertainties in the reducible background #
#############################################
stat_reducible_2016 = {
    "em" : 1.16,
    "et" : 1.13,
    "mt" : 1.16,
    "tt" : 1.15
}

stat_reducible_2017 = {
    "em" : 1.13,
    "et" : 1.14,
    "mt" : 1.17,
    "tt" : 1.15
}

stat_reducible_2018 = {
    "em" : 1.17,
    "et" : 1.09,
    "mt" : 1.11,
    "tt" : 1.12
}

stat_reducible_Run2 = {
    "2016" : stat_reducible_2016,
    "2017" : stat_reducible_2017,
    "2018" : stat_reducible_2018
}

nonclosure_reducible = {
    "em" : 1.50,
    "et" : 1.30,
    "mt" : 1.20,
    "tt" : 1.20
}

# add JES uncertainty once available
expUnc = {
    'unclMET' : 'CMS_scale_met_unclustered',
    'tauID0' : 'CMS_eff_t_1prong',
    'tauID1' : 'CMS_eff_t_1prong1pizero',
    'tauID10' : 'CMS_eff_t_3prong',
    'tauID11': 'CMS_eff_t_3prong1pizero',
    'tauES' : 'CMS_scale_t',
    'efake' : 'CMS_azh_efake',
    'mfake' : 'CMS_azh_mfake',
    'eleES' : 'CMS_scale_e',
    'muES' : 'CMS_scale_m',
    'pileup' : 'CMS_pileup',
    'l1prefire' : 'CMS_l1prefire',
    'eleSmear' : 'CMS_res_e',
    'JES' : 'CMS_scale_j',
    'JER' : 'CMS_res_j'
}

fakeUnc = ['bin1','bin2','bin3']

h_channel_map={
    'eeem' : 'em',
    'eeet' : 'et',
    'eemt' : 'mt',
    'eett' : 'tt',
    'mmem' : 'em',
    'mmet' : 'et',
    'mmmt' : 'mt',
    'mmtt' : 'tt'
}

# decorrelating instrumental uncs across years
def DecorrelateUncertainties(cb,year,channel):
    for unc in expUnc:
        cb.cp().RenameSystematic(cb,unc,expUnc[unc]+"_"+year)

parser = argparse.ArgumentParser(description="Datacards producer for AZh analysis")
parser.add_argument("-year", "--year", required=True,help=""" year : 2016, 2017 or 2018 """,choices=utils.years)
parser.add_argument("-btag", "--btag", required=True,help=""" category : btag or 0btag """,choices=utils.azh_cats)
parser.add_argument("-mass", "--mass", required=True,help=""" mass of A boson """,choices=utils.azh_masses)
parser.add_argument("-model", "--model", default="2POI",help=""" model : ggA, bbA or 2POI""",choices=["ggA","bbA","2POI"])
parser.add_argument("-folder","--folder", default="datacards",help=""" folder where datacards are saved""")
parser.add_argument("-all_channels","--all_channels",action='store_true',help=""" including all channels with em""")
parser.add_argument("-no_bbb","--no_bbb", action='store_true',help=""" parameter to drop MC statistical uncertainties""")
args = vars(parser.parse_args())

year, mass, btag_label, model, folder = args["year"], args["mass"], args["btag"], args["model"], args["folder"]

cats = [
    (1, "eeet"),
    (2, "eemt"),
    (3, "eett"),
    (4, "mmet"),
    (5, "mmmt"),
    (6, "mmtt"),
]

if args["all_channels"]:
    cats.append((7, 'eeem'))
    cats.append((8, 'mmem'))

auto_mc = True
if args["no_bbb"]:
    auto_mc = False

mc_bkgd = [ 
    "ggZZ",
    "ZZ",
    "TTZ",
    "VVV",
    "ZHtt",
    "TTHtt",
    "ZHWW",
    "ggZHWW",
#    "ggHZZ", -> negligible
#    "ggHtt", -> cannot produce 4 genuine charged leptons
#    "VFBHtt", -> cannot produce 4 genuine charged leptons
#    "WHtt", -> cannot produce 4 genuine charged leptons
#    "ggHWW", -> cannot produce 4 genuine charged leptons
#    "VBFHWW", -> cannot produce 4 genuine charged leptons
#    "TTW", -> cannot produce 4 genuine charged leptons
#    "TT" -> cannot produce 4 genuine charged leptons
]
reducible = ["reducible"]

signals = []
if model=="bbA":
    signals.append("bbA")
elif model=="ggA":
    signals.append("ggA")
else:
    signals.append("bbA")
    signals.append("ggA")


cb = ch.CombineHarvester()

cb.AddObservations(["*"], ["azh"], [year], [btag_label], cats)
cb.AddProcesses([mass], ["azh"], [year], [btag_label], signals, cats, True)
cb.AddProcesses(["*"], ["azh"], [year], [btag_label], reducible, cats, False)
cb.AddProcesses(["*"], ["azh"], [year], [btag_label], mc_bkgd, cats, False)

mc_processes = signals + mc_bkgd
# luminosity
if year=='2016':
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Uncorrelated_2016','lnN', ch.SystMap()(1.010))
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Correlated','lnN', ch.SystMap()(1.006)) 
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2016','lnN', ch.SystMap()(1.010))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.004))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.009))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Ghosts_And_Satellites','lnN', ch.SystMap()(1.004))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Dynamic_Beta','lnN', ch.SystMap()(1.005))

if year=='2017':
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Uncorrelated_2017','lnN', ch.SystMap()(1.020))
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Correlated','lnN', ch.SystMap()(1.009))
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Correlated1718','lnN', ch.SystMap()(1.006))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2017','lnN', ch.SystMap()(1.020))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.004))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.008))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Current_Calibration','lnN', ch.SystMap()(1.003))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Length_Scale','lnN', ch.SystMap()(1.003))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Ghosts_And_Satellites','lnN', ch.SystMap()(1.001))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Dynamic_Beta','lnN', ch.SystMap()(1.005))

if year=='2018':
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Uncorrelated_2018','lnN', ch.SystMap()(1.015))
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Correlated','lnN', ch.SystMap()(1.02))
    cb.cp().process(mc_processes).AddSyst(cb,'CMS_lumi_13TeV_Correlated1718','lnN', ch.SystMap()(1.002))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2018','lnN', ch.SystMap()(1.015))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.002))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.02))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Current_Calibration','lnN', ch.SystMap()(1.002))
#    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Length_Scale','lnN', ch.SystMap()(1.002))

# Higgs tau tau PU alphas
cb.cp().signals().AddSyst(cb, "BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062))
cb.cp().process(["ggHtt", "VBFHtt", "WHtt", "ZHtt", "TTHtt"]).AddSyst(
    cb, "BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062)
)
cb.cp().signals().AddSyst(cb, "BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099))
cb.cp().process(["ggHtt", "VBFHtt", "WHtt", "ZHtt", "TTHtt"]).AddSyst(
    cb, "BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099)
)
cb.cp().signals().AddSyst(cb, "BR_htt_THU", "lnN", ch.SystMap()(1.017))
cb.cp().process(["ggHtt", "VBFHtt", "WHtt", "ZHtt", "TTHtt"]).AddSyst(
    cb, "BR_htt_THU", "lnN", ch.SystMap()(1.017)
)

# Higgs WW PU alphas
cb.cp().process(["ggHWW", "VBFHWW", "WHWW", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "BR_hww_PU_alphas", "lnN", ch.SystMap()(1.0066)
)
cb.cp().process(["ggHWW", "VBFHWW", "WHWW", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "BR_hww_PU_mq", "lnN", ch.SystMap()(1.0099)
)
cb.cp().process(["ggHWW", "VBFHWW", "WHWW", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "BR_hww_THU", "lnN", ch.SystMap()(1.0099)
)

# CMS electron efficiencies
# 1.5% correlated across years
syst_map = ch.SystMap("bin_id")([1], 1.045)([2, 3], 1.03)([4], 1.015)#([5, 6], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e", "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_e", "lnN", syst_map)

# CMS electron trigger
# 1.5 uncertainty correlated across years
syst_map = ch.SystMap("bin_id")([1, 2, 3], 1.015)#([4, 5, 6], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_trigger_e", "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_trigger_e", "lnN", syst_map)


# CMS muon efficiencies
# 1.5% correlated across years
syst_map = ch.SystMap("bin_id")([5], 1.045)([4, 6], 1.03)([2], 1.015)#([1, 3], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m", "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_m", "lnN", syst_map)

# CMS muon trigger
# 1.5% correlated across years
syst_map = ch.SystMap("bin_id")([4, 5, 6], 1.015)#([1, 2, 3], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_trigger_m", "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_trigger_m", "lnN", syst_map)

# refs:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV

# cross sections
cb.cp().process(["ggZZ"]).AddSyst(cb, "CMS_azh_ggzzXsec", "lnN", ch.SystMap()(1.15))
cb.cp().process(["TT"]).AddSyst(cb, "CMS_azh_tjXsec", "lnN", ch.SystMap()(1.06))
cb.cp().process(["TTW","TTZ"]).AddSyst(cb, "CMS_azh_ttvXsec", "lnN", ch.SystMap()(1.25))
cb.cp().process(["ZZ", "WZ"]).AddSyst(cb, "CMS_azh_vvXsec", "lnN", ch.SystMap()(1.05))
cb.cp().process(["VVV"]).AddSyst(cb, "CMS_azh_vvvXsec", "lnN", ch.SystMap()(1.25))

# QCD scale VH
cb.cp().process(
    [
        "WHtt",
        "WHWW",
    ]
).AddSyst(cb, "QCDscale_VH", "lnN", ch.SystMap()(1.008))
cb.cp().process(["ZHtt", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "QCDscale_ZH", "lnN", ch.SystMap()(1.009)
)
cb.cp().process(["ggHtt", "ggHWW", "ggHZZ"]).AddSyst(
    cb, "QCDscale_ggH", "lnN", ch.SystMap()(1.039)
)
cb.cp().process(["VBFHtt", "VBFHWW"]).AddSyst(
    cb, "QCDscale_qqH", "lnN", ch.SystMap()(1.005)
)
cb.cp().process(["TTHtt"]).AddSyst(cb, "QCDscale_ttH", "lnN", ch.SystMap()(1.08))

# pdf Higgs
cb.cp().process(["WHtt", "WHWW"]).AddSyst(
    cb, "pdf_Higgs_qqbar", "lnN", ch.SystMap()(1.018)
)
cb.cp().process(["ZHtt", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "pdf_Higgs_qqbar", "lnN", ch.SystMap()(1.013)
)
cb.cp().process(["ggHtt", "ggHWW", "ggHZZ"]).AddSyst(
    cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.032)
)
cb.cp().process(["VBFHtt", "VBFHWW"]).AddSyst(
    cb, "pdf_Higgs_qqbar", "lnN", ch.SystMap()(1.021)
)
cb.cp().process(["TTHtt"]).AddSyst(cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.036))

# add shape systematics
bkgd = mc_bkgd + signals
bkgd_mod = [b for b in bkgd if "ggHWW" not in b]
bkgd_tauID = [b for b in bkgd]

#for unc in fakeUnc:
#    cb.cp().process(reducible).AddSyst(cb, unc, "shape", ch.SystMap()(1.00))

# btag uncertainties
btagFile = ROOT.TFile('jet_systematics/systematics_%s_bkg.root'%(year))
btagmap = {
    'btag' : 'eff_b',
    'mistag' : 'mistag_b'
}
for proc in mc_bkgd:
    for cat in cats:
        for sys in ['btag','mistag']:
            chan = cat[1]
            binid = cat[0]
            histBtagName = '%s_%s_%s_%s'%(proc,chan,args['btag'],sys)
            histBtag = btagFile.Get(histBtagName)
            value = histBtag.GetBinContent(2) - 1.0
            value_correlated = 1.2*value + 1.0
            value_uncorrelated = 0.8*value + 1.0
            value_corr = float(int(1000*value_correlated))/1000.0
            value_uncorr = float(int(1000*value_uncorrelated))/1000.0
            cb.cp().process([proc]).bin_id([binid]).AddSyst(cb, "CMS_azh_"+btagmap[sys]+"_"+year, "lnN", ch.SystMap()(value_uncorr))
            cb.cp().process([proc]).bin_id([binid]).AddSyst(cb, "CMS_azh_"+btagmap[sys], "lnN", ch.SystMap()(value_corr))

btagFile = ROOT.TFile('jet_systematics/systematics_%s_sig.root'%(year))
for proc in signals:
    for cat in cats:
        for sys in ['btag','mistag']:
            chan = cat[1]
            binid = cat[0]
            histBtagName = '%s%s_%s_%s_%s'%(proc,mass,chan,args['btag'],sys)
            histBtag = btagFile.Get(histBtagName)
            value = histBtag.GetBinContent(2) - 1.0
            value_correlated = 1.2*value + 1.0
            value_uncorrelated = 0.8*value + 1.0
            value_corr = float(int(1000*value_correlated))/1000.0
            value_uncorr = float(int(1000*value_uncorrelated))/1000.0
            cb.cp().process([proc]).bin_id([binid]).AddSyst(cb, "CMS_azh_"+btagmap[sys]+"_"+year, "lnN", ch.SystMap()(value_uncorr))
            cb.cp().process([proc]).bin_id([binid]).AddSyst(cb, "CMS_azh_"+btagmap[sys], "lnN", ch.SystMap()(value_corr))


# JES uncertainty
cb.cp().process(bkgd).AddSyst(cb, "JES", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd).AddSyst(cb, "JER", "shape", ch.SystMap()(1.00))

cb.cp().process(bkgd_tauID).AddSyst(cb, "tauID0", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd_tauID).AddSyst(cb, "tauID1", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd_tauID).AddSyst(cb, "tauID10", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd_tauID).AddSyst(cb, "tauID11", "shape", ch.SystMap()(1.00))
cb.cp().process([b for b in bkgd_mod if ("ggZHWW" not in b)]).AddSyst(
    cb, "tauES", "shape", ch.SystMap()(1.00)
)
cb.cp().process(
    [b for b in bkgd if (("ZHWW" not in b) and ("ggZHWW" not in b) and ("WZ" not in b))]
).AddSyst(cb, "unclMET", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd).AddSyst(cb, "pileup", "shape", ch.SystMap()(1.00))
cb.cp().process([b for b in bkgd if ("WZ" not in b)]).AddSyst(
    cb, "l1prefire", "shape", ch.SystMap()(1.00)
)

# reducible background
stat_unc = stat_reducible_Run2[year]

# systematicc uncertainties in reducible background
for cat in cats:
    ib = cat[0]
    ib_name = cat[1]
    h_channel = h_channel_map[ib_name]
    value = stat_unc[h_channel]
#    print(ib_name,h_channel,value)
    cb.cp().process(['reducible']).channel([btag_label]).bin_id([ib]).AddSyst(cb, "CMS_azh_stat_fakes_"+ib_name+"_"+year,"lnN", ch.SystMap()(value))
    value = nonclosure_reducible[h_channel]
#    print(ib_name,h_channel,value)
    cb.cp().process(['reducible']).channel([btag_label]).bin_id([ib]).AddSyst(cb, "CMS_azh_sys_fakes_"+h_channel,"lnN", ch.SystMap()(value))

cb.cp().process(bkgd).AddSyst(cb, "eleES", "shape", ch.SystMap()(1.00)) 
cb.cp().process(bkgd).AddSyst(cb, "eleSmear", "shape", ch.SystMap()(1.00))
#cb.cp().process(bkgd).AddSyst(cb, "muES", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd).AddSyst(cb, "efake", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd).AddSyst(cb, "mfake", "shape", ch.SystMap()(1.00))

# add bin uncertainty systematics
mc = uproot.open(
#    "/uscms_data/d3/jdezoort/AZh_columnar/CMSSW_10_2_9/"
    os.getenv('CMSSW_BASE') + '/src/AZh/combine/root_files/MC_data_%s_%s.root'%(btag_label,year)
)
# for b in np.arange(15):
#    for i in cats:
#        cat, num = i[1], i[0]
#        #nums = [1, 2, 3, 4, 5, 6, 7, 8]
#        syst_map = ch.SystMap("bin_id")([num], 1.0)#([n for n in nums if n!=num], 0.0)
#        proc = mc_bkgd + reducible
#        keys = [k.decode('utf-8').strip(";1") for k in mc[cat].keys()]
#        #proc = [p for p in proc if f"{p}_bin{b}Up" in keys]
#        #print(cat, f"bin{b}", proc)
#        #cb.cp().process(proc).AddSyst(cb, f"bin{b}", "shape", syst_map)
#        for p in proc:
#            if f"{p}_{p}-{cat}-bin{b}Up" not in keys: continue
#            if "mmet" in cat and b==1 and "WZ" in p: continue
#            print(p, cat, b)
#            cb.cp().process([p]).AddSyst(cb, f"{p}-{cat}-bin{b}", "shape", syst_map)

# add MC bin-by-bin uncertainties
if auto_mc:
    cb.AddDatacardLineAtEnd("* autoMCStats 0")

# extract shapes
cb.cp().backgrounds().ExtractShapes(
    (
#        "/uscms_data/d3/jdezoort/AZh_columnar/CMSSW_10_2_9/src/"
        os.getenv('CMSSW_BASE') + '/src/AZh/combine/root_files/MC_data_%s_%s.root'%(btag_label,year)
    ),
    "$BIN/$PROCESS",
    "$BIN/$PROCESS_$SYSTEMATIC",
)

cb.cp().signals().ExtractShapes(
    (
        #        "/uscms_data/d3/jdezoort/azh_columnar/CMSSW_10_2_9/src/"
        os.getenv('CMSSW_BASE') + '/src/AZh/combine/root_files/signal_%s_%s_%s.root'%(mass,btag_label,year)
    ),
    "$BIN/$PROCESS",
    "$BIN/$PROCESS_$SYSTEMATIC",
)

#ch.SetStandardBinNames(cb)

DecorrelateUncertainties(cb,year,btag_label)

writer = ch.CardWriter(
    "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN_$MASS.txt",
    "$TAG/$ANALYSIS_$ERA_$CHANNEL_$BIN_$MASS.root",
)

writer.WriteCards('%s/%s/%s/'%(folder,year,mass), cb)
writer.WriteCards('%s/Run2/%s/'%(folder,mass), cb)

#print('Done cards for year : %s -- category : %s -- mass : %s -- channel '%(year,btag_label,mass))


