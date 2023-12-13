# A->Zh->(ll)(tautau) : statistical analysis 

## Installation

The statistical inference of the AZh search results requires [Higgs combination package](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git),  [CombineHarvester toolkit](https://cms-analysis.github.io/CombineHarvester/index.html)  and  [python analysis code](https://github.com/raspereza/AZh.git). We recommend to download also [datacards of the previous analysis HIG-18-023](https://gitlab.cern.ch/cms-analysis/hig/HIG-18-023).

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
Datacards for Run2 combination will be output into folders `datacards/Run2/$mass`
At the next step workspaces to be used by [combine tool](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit), need to be produce. This is done with script [CreateWorkspaces.py](https://github.com/raspereza/AZh/blob/main/combine/CreateWorkspaces.py)
```
./CreateCards.py --year $year
```

## Running limits

## Running impacts

## Running GoF tests

## Running fits