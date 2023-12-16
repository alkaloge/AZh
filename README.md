# A->Zh->(ll)(tautau) : statistical analysis 

This documentation describes  statistical inference package used in the analysis searching for heavy pseudoscalar boson A predicted by the models with extended Higgs sector in the A->Zh->(ee+mm)(tau+tau) decay channel. The search uses ultra-legacy data collected with the CMS detector at the CERN Large Hadron Collider.

## Installation

The statistical inference of the AZh search results requires [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git),  [CombineHarvester toolkit](https://cms-analysis.github.io/CombineHarvester/index.html)  and  [python analysis code](https://github.com/raspereza/AZh.git). We recommend to download also [datacards of the previous analysis HIG-18-023](https://gitlab.cern.ch/cms-analysis/hig/HIG-18-023) for comparison.

Installation proceeds as follows:
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_13
cd CMSSW_10_6_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git checkout v8.2.0
cd ../..
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
git clone https://github.com/raspereza/AZh.git AZh
scramv1 b -j 4
```

Root files with shapes to be used as inputs for datacards producer, are located in the folder [$CMSSW_BASE/src/AZh/combine/root_files](https://github.com/raspereza/AZh/tree/main/combine/root_files)

After installation is complete change to the directory [$CMSSW_BASE/src/AZh/combine](https://github.com/raspereza/AZh/tree/main/combine). All scripts will be run from this directory.

Retrieve datacards of the HIG-18-023 analysis:
```
cd $CMSSW_BASE/src/AZh/combine
git clone https://gitlab.cern.ch/cms-analysis/hig/HIG-18-023 HIG-18-023
```

Then execute macro [Setup.py](https://github.com/raspereza/AZh/blob/main/combine/Setup.py)
```
./Setup.py
```

The macro [Setup.py](https://github.com/raspereza/AZh/blob/main/combine/Setup.py) performs the following actions :
1. It merges RooT files with data and background templates into one since [CombineHarvester](https://cms-analysis.github.io/CombineHarvester/index.html) is looking for data distributions and background templates in the same file.
2. It fixes bins with negative content in signal and backgroun templates.
3. It creates in the current directory subfolders `figures` and `jobs` where png files and batch job scripts will be put.


## Creation of datacards and workspaces

Datacards for one signal mass point are created by macro [make_datacards.py](). It is executed with several parameters:
```
./make_datacards.py --year $year --btag $btag --mass $mass --bbb $bin-by-bin --outdir $outdir --proc $proc 
```
where
* `$year : {2016, 2017, 2018}`;
* `$btag : {btag, 0btag}`
* `$mass :` mass hypothesis
* `$bin-by-bin : {auto_mc, none}`; if option `auto_mc` is specified bin-by-bin MC statistical uncertainties are automatically included into statistical inference, if option `none` is specified, bin-by-bin MC statistical uncertainties are ignored. `auto_mc` is set by default and recommended
* `$proc : {ggA,bbA, all}` : specifies signal model. If this argument is set to `ggA`, then only ggA process is considered as signal and other process is ignored. If argument is set to `bbA`, then only `bbA` process is considered as signal and other is ignored. Option `all` is set by default and recommended, meaning that both processes are included in the signal model.
* `$outdir` : output folder where datacards will be put. Default setting is `datacards` 

Out of six parameters, three must be specified by user : `$year` `$btag` and `$mass`. 

Datacards can be produced for all eras, all signal mass points and for both `btag` and `0btag` categories in one go by using script [CreateCards.py](https://github.com/raspereza/AZh/blob/main/combine/CreateCards.py)
```
./CreateCards.py
```

For each $year and $mass hypothesis datacards will be put in the folder `datacards/$year/$mass`.
Datacards for Run2 combination will be output into folders `datacards/Run2/$mass`.
At the next step workspaces to be used by [combine tool](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit), need to be produce. This is done with script [CreateWorkspaces.py](https://github.com/raspereza/AZh/blob/main/combine/CreateWorkspaces.py)
```
./CreateWorkspaces.py --year $year
```
with parameter `$year` being one of three years: 2016, 2017, 2018 or Run2 for combination. Parameter `$year` is set to Run2 by default. Workspace for a single mass point and year is created for the signal model with two processes - `ggA` and `bbA`.  
Macro `CreateWorkspaces.py` loops over all signal mass points. To produce workspace for one mass point macro it calls bash script [CreateWorkspace.bash](https://github.com/raspereza/AZh/blob/main/combine/CreateWorkspace.bash), which in its turn execuites combine utility of the [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git). For each `$year` and `$mass`, workspace is stored in the folder `datacards/$year/$mass` under the name `ws.root`. Workspaces for Run2 combination are put in folders `datacards/Run2/$mass` under the same name. Models implemented in workspaces contain two parameters of interest (POI): rate of the process ggA (r_ggA) and rate of the process bbA (r_bbA). Running workspaces for one era and especially for Run2 combination may takes time. Be patient.


## Creating workspaces for HIG18-023 analysis 

To enable comparison with the published HIG-18-023 analysis, datacards for this analysis need to be also created. It is done using bash script [CombineCards_HIG18023.bash](https://github.com/raspereza/AZh/blob/main/combine/CombineCards_HIG18023.bash). Workspaces for the HIG-18-023 analysis will are put in folders `HIG-18-023/$mass`.

## Checking shapes and systematic variations of MC templates

Shape and variations of MC templates can be checked with macro []()

## Running limits

Example below shows how to compute expected limits on the rate of the process ggA, while rate of the bbA process is set to zero. 
```
combine -M AsymptoticLimits -d datacards/Run2/1000/ws.root \ 
--setParameters r_bbA=0,r_ggA=0 \
--setParameterRanges r_ggA=-50,50 \ 
--redefineSignalPOIs r_ggA \
--freezeParameters r_bbA \
--rAbsAcc 0 --rRelAcc 0.0005 \ 
--X-rtd MINIMIZER_analytic \
--cminDefaultMinimizerStrategy 0 \
--cminDefaultMinimizerTolerance 0.01 \ 
--noFitAsimov -t -1 \ 
-n ".azh_Run2_bbA" -m 1000 \
```
In this example, limits are calculated for the combined Run2 analysis and for mass hypothesis of mA = 1000 GeV, implying that workspace is located in folder `datacards/Run2/1000`. The rate of the bbA process is fixed to zero by settings `--setParameters r_bbA=0` and `--freezeParameters r_bbA`. The flags `--noFitAsimov -t -1` instructs combine utility to compute expected limits without fitting signal+background model to data. The flag `-n ".azh_Run2_bbA"` defined the suffix to be assigned to the output root file with the results of limit computation. In this example output root file will be saved under the name `higgsCombine.azh_Run2_ggA.AsymptoticLimits.mH1000.root`. All other parameters steer the fit and limit finding algorithms. One should swap POIs `r_ggA` and `r_bbA` in the command above to compute limit on the rate of bbA process with the rate of ggA fixed to zero. 

To compute limits on the ggA rate while profiling in the fit the rate of bbA process, one has to remove flag  `--freezeParameters r_bbA` and allow parameter `r_bbA` to float freely in a reasonably large range : `--setParameterRanges r_ggA=-50,50:r_bbA=-50,50`.

To compute observed limits one needs to remove the flag `--noFitAsimov -t -1`.

Macro [RunLimits.py](https://github.com/raspereza/AZh/blob/main/combine/RunLimits.py) automatises computation of limits with `combine` utility. It is executed with the following parameters:
```
./RunLimits.py --analysis $analysis --year $year --type ${exp,obs} --freezeOtherPOI ${yes,no} --outdir $outdir --mass $mass
```
where
* `$analysis = {hig18023, azh}` : if set to `hig18023` or `HIG18023` limits are computed for the HIG18-023 analysis, if set to `azh` or `AZh` - limits are computed for the current analysis. Default = `azh`.
* `$year = {2016, 2017, 2018, Run2}`; Default = `Run2`.
* `$type = {exp,obs} ` : expected to observed limits.  Default = `exp`.
* `--freezeOtherPOI = {yes,no}` : set other POI to zero or float it freely. Default = `yes`.
* `$outdir ` : folder where results of limit computation will be stored. Default = `limits`.
 

## Running impacts

## Running GoF tests

## Running fits

## Running fits with two floating rates: r_ggA and r_bbA