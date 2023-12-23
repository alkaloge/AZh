#!/usr/bin/env python

import argparse
import os

import AZh.combine.utilsAZh as utils
import CombineHarvester.CombineTools.ch as ch
import uproot

cats = [
    (1, "eeem"),
    (2, "eeet"),
    (3, "eemt"),
    (4, "eett"),
    (5, "mmem"),
    (6, "mmet"),
    (7, "mmmt"),
    (8, "mmtt"),
]


expUnc = ['unclMET','tauID0','tauID1','tauID10','tauID11','tauES','efake','mfake','eleES','muES','pileup','l1prefire','eleSmear']

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
        cb.cp().RenameSystematic(cb,unc,unc+"_"+year)
    for unc in fakeUnc:
        for cat in cats:
            ib = cat[0]
            ib_name = cat[1]
            h_channel = h_channel_map[ib_name]
            cb.cp().channel([channel]).bin_id([ib]).RenameSystematic(cb,unc,"%s_%s_%s"%(h_channel,unc,year))

parser = argparse.ArgumentParser(description="Datacards producer for AZh analysis")
parser.add_argument("-year", "--year", required=True,help=""" year : 2016, 2017 or 2018 """,choices=utils.years)
parser.add_argument("-btag", "--btag", required=True,help=""" category : btag or 0btag """,choices=utils.azh_cats)
parser.add_argument("-mass", "--mass", required=True,help=""" mass of A boson """,choices=utils.azh_masses)
parser.add_argument("-no_bbb","--no_bbb", action='store_true',help=""" parameter to drop MC statistical uncertainties""")
args = vars(parser.parse_args())

year, mass, btag_label = args["year"], args["mass"], args["btag"]
outdir=utils.DatacardsFolder
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
#    "ggHtt", -> cannot produce 4 genuine charged leptons
#    "VFBHtt", -> cannot produce 4 genuine charged leptons
#    "WHtt", -> cannot produce 4 genuine charged leptons
#    "ggHWW", -> cannot produce 4 genuine charged leptons
#    "ggHZZ", -> negligible
#    "VBFHWW", -> cannot produce 4 genuine charged leptons
#    "TTW", -> cannot produce 4 genuine charged leptons
#    "TT" -> canno produce 4 genuine charged leptons
]
reducible = ["reducible"]

signals = ["bbA","ggA"]

cb = ch.CombineHarvester()

cb.AddObservations(["*"], ["azh"], [year], [btag_label], cats)
cb.AddProcesses([mass], ["azh"], [year], [btag_label], signals, cats, True)
cb.AddProcesses(["*"], ["azh"], [year], [btag_label], reducible, cats, False)
cb.AddProcesses(["*"], ["azh"], [year], [btag_label], mc_bkgd, cats, False)

mc_processes = signals + mc_bkgd
# luminosity
if year=='2016':
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2016','lnN', ch.SystMap()(1.010))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.004))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.009))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Ghosts_And_Satellites','lnN', ch.SystMap()(1.004))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Dynamic_Beta','lnN', ch.SystMap()(1.005))

if year=='2017':
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2017','lnN', ch.SystMap()(1.020))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.004))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.008))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Current_Calibration','lnN', ch.SystMap()(1.003))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Length_Scale','lnN', ch.SystMap()(1.003))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Ghosts_And_Satellites','lnN', ch.SystMap()(1.001))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Dynamic_Beta','lnN', ch.SystMap()(1.005))

if year=='2018':
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Uncorrelated_2018','lnN', ch.SystMap()(1.015))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Beam_Deflection','lnN', ch.SystMap()(1.002))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_X_Y_Factorization','lnN', ch.SystMap()(1.02))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Beam_Current_Calibration','lnN', ch.SystMap()(1.002))
    cb.cp().process(mc_processes).AddSyst(cb,'lumi_13TeV_Length_Scale','lnN', ch.SystMap()(1.002))


# Obsolete scheme
#cb.cp().signals().AddSyst(cb, "CMS_lumi_13TeV_2016", "lnN", ch.SystMap()(1.01))
#cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_lumi_13TeV_2016", "lnN", ch.SystMap()(1.01))
#cb.cp().signals().AddSyst(cb, "CMS_lumi_13TeV_correlated", "lnN", ch.SystMap()(1.006))
#cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_lumi_13TeV_correlated", "lnN", ch.SystMap()(1.006))

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

# CMS_NNLO_ggZZ
cb.cp().process(["ggZZ"]).AddSyst(cb, "CMS_NNLO_ggZZ", "lnN", ch.SystMap()(1.1))

# CMS electron efficiencies
# 2% correlated part and 1% decorrelated
syst_map = ch.SystMap("bin_id")([1, 2], 1.03)([3, 4], 1.02)([5, 6], 1.01)([7, 8], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e_"+year, "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_e_"+year, "lnN", syst_map)

syst_map = ch.SystMap("bin_id")([1, 2], 1.06)([3, 4], 1.04)([5, 6], 1.02)([7, 8], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_e_"+year, "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_e", "lnN", syst_map)


# CMS muon efficiencies
# 1.5% correlated and 1% decorrelated
syst_map = ch.SystMap("bin_id")([5, 7], 1.03)([6, 8], 1.02)([1, 3], 1.01)([2, 4], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m_"+year, "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_m_"+year, "lnN", syst_map)

syst_map = ch.SystMap("bin_id")([5, 7], 1.06)([6, 8], 1.04)([1, 3], 1.02)([2, 4], 1.0)
cb.cp().process(mc_bkgd).AddSyst(cb, "CMS_eff_m_"+year, "lnN", syst_map)
cb.cp().signals().AddSyst(cb, "CMS_eff_m", "lnN", syst_map)

# refs:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV

# cross sections
cb.cp().process(["ggZZ"]).AddSyst(cb, "CMS_xsec_ggZZ", "lnN", ch.SystMap()(1.1))
cb.cp().process(["TT"]).AddSyst(cb, "CMS_xsec_top", "lnN", ch.SystMap()(1.06))
cb.cp().process(["TTW"]).AddSyst(cb, "CMS_xsec_ttW", "lnN", ch.SystMap()(1.25))
cb.cp().process(["TTZ"]).AddSyst(cb, "CMS_xsec_ttZ", "lnN", ch.SystMap()(1.25))

cb.cp().process(["ZZ", "WZ"]).AddSyst(cb, "CMS_xsec_vv", "lnN", ch.SystMap()(1.048))
cb.cp().process(["VVV"]).AddSyst(cb, "CMS_xsec_vvv", "lnN", ch.SystMap()(1.25))

# QCD scale VH
cb.cp().process(
    [
        "WHtt",
        "WHWW",
    ]
).AddSyst(cb, "QCDscale_VH", "lnN", ch.SystMap()(1.008))
cb.cp().process(["ZHtt", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "QCDscale_VH", "lnN", ch.SystMap()(1.009)
)
cb.cp().process(["ggHtt", "ggHWW", "ggHZZ"]).AddSyst(
    cb, "QCDscale_ggh", "lnN", ch.SystMap()(1.039)
)
cb.cp().process(["VBFHtt", "VBFHWW"]).AddSyst(
    cb, "QCDscale_qqh", "lnN", ch.SystMap()(1.005)
)
cb.cp().process(["TTHtt"]).AddSyst(cb, "QCDscale_tth", "lnN", ch.SystMap()(1.08))

# pdf Higgs
cb.cp().process(["WHtt", "WHWW"]).AddSyst(
    cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.018)
)
cb.cp().process(["ZHtt", "ZHWW", "ggZHWW"]).AddSyst(
    cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.013)
)
cb.cp().process(["ggHtt", "ggHWW", "ggHZZ"]).AddSyst(
    cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.032)
)
cb.cp().process(["VBFHtt", "VBFHWW"]).AddSyst(
    cb, "pdf_Higgs_qqbar", "lnN", ch.SystMap()(1.021)
)
cb.cp().process(["TTHtt"]).AddSyst(cb, "pdf_Higgs_ttH", "lnN", ch.SystMap()(1.036))

# add shape systematics
bkgd = mc_bkgd + signals
bkgd_mod = [b for b in bkgd if "ggHWW" not in b]
bkgd_tauID = [b for b in bkgd]

for unc in fakeUnc:
    cb.cp().process(reducible).AddSyst(cb, unc, "shape", ch.SystMap()(1.00))

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

cb.cp().process(bkgd).AddSyst(cb, "eleES", "shape", ch.SystMap()(1.00)) 
cb.cp().process(bkgd).AddSyst(cb, "eleSmear", "shape", ch.SystMap()(1.00))
cb.cp().process(bkgd).AddSyst(cb, "muES", "shape", ch.SystMap()(1.00))
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
writer.WriteCards('%s/%s/%s/'%(outdir,year,mass), cb)
writer.WriteCards('%s/Run2/%s/'%(outdir,mass), cb)

print('Done cards for year : %s -- category : %s -- mass : %s'%(year,btag_label,mass))


