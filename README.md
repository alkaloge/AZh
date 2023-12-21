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
./make_datacards.py --year $year --btag $btag --mass $mass
```
where
* `$year : {2016, 2017, 2018}`;
* `$btag : {btag, 0btag}`
* `$mass :` mass hypothesis

Datacards for a given year and mass are stored in the folder
* `datacards/$year/$mass` : for signal model with 2 POIs;
* `datacards_$proc/$year/$mass` : for signal model with only one process `$proc={bbA,ggA}`.

Combined Run2 datacards are put in folders 
* `datacards/Run2/$mass` : for signal model with 2 POIs;
* `datacards_$proc/Run2/$mass` : for signal model with only one process `$proc={bbA,ggA}`.

By default datacards are created with option `* autoMCStats 0` meaning that bin-by-bin MC statistical uncertainties are automatically included into uncertainty model. To disable MC this option, script should be run with additional flag `--no_bbb`

Datacards can be produced for all years and all mass points in one go by executing script [CreateCards.py](https://github.com/raspereza/AZh/blob/main/combine/CreateCards.py)
```
./CreateCards.py
```
Running datacards for all years and mass points may take awhile.

For each $year and $mass hypothesis datacards will be put in the folder `datacards/$year/$mass`.
Datacards for Run2 combination will be output into folders `datacards/Run2/$mass`.
At the next step workspaces to be used by [combine tool](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit), need to be produce. This is done with script [CreateWorkspaces.py](https://github.com/raspereza/AZh/blob/main/combine/CreateWorkspaces.py)
```
./CreateWorkspaces.py --year $year --mass $mass 
```
where
* `$year` : 2016, 2017, 2018 or Run2 for combination. Parameter `$year` is set to Run2 by default. 
* `$mass` : mA (default = 1000). One can produce workspaces for all mass points in sequence by setting `$mass` to `all` 

For each $year and $mass workspaces are put in the folder `datacards/$year/$mass` under the name `ws.root`. Workspaces for Run2 combination are put in folders `datacards/Run2/$mass` under the same name. 

Signal model includes two  parameters of interest (POI): rate of the process ggA (r_ggA) and rate of the process bbA (r_bbA). Running workspaces for one era and especially for Run2 combination may takes time. Be patient.

## Creating workspaces for HIG18-023 analysis 

To enable comparison with the published HIG-18-023 analysis, datacards for this analysis need to be also created. It is done using bash script [CombineCards_HIG18023.bash](https://github.com/raspereza/AZh/blob/main/combine/CombineCards_HIG18023.bash). Workspaces for the HIG-18-023 analysis will are put in folders `HIG-18-023/$mass`.

## Checking shapes and systematic variations of MC templates

Shapes and systematic variations of MC templates can be plotted with macro [CheckTemplate.py](https://github.com/raspereza/AZh/blob/main/combine/CheckTemplate.py) with the following arguments
* `--analysis` - analysis : azh (our analysis) or hig18026 (HIG-18-023);
* `--year` - 2016, 2017 or 2018;
* `--channel` - channels : eeem, eeet, eemt, eett, mmem, mmet, mmmt or mmtt;
* `--cat` - event category : 0btag or btag;
* `--template` - name of MC template, e.g. ZZ, ggZ, TTZ, bbA, ggA, etc., when "all" is specified, all templates are plotted;
* `--mass` - mass hypothesis mA (for signal templates);
* `--sys` - name of systematic uncertainty, e.g. eleES, tauES, tauID0, unclMET, etc., when "all" is specified all systematic variations are plotted;
* `--xmin` - lower edge of x axis (default = 200);
* `--xmax` - upper edge of x axis (default = 1000);

Optional (boolean) flags
* `--logx` - log scale is set for x axis 
* `--dry_run` - dry run of the routine printing out available options for input arguments
* `--verbosity` - detailed printout is activates

Few examples of usage are given below
```
./CheckTemplate.py --analysis azh --year 2018 --cat btag --channel mmmt --template ZZ --sys eleES
```
With this command the ZZ template along with up/down variations related to uncertainty `eleES` will be plotted from the datacards of our analysis (azh) into file
*`$CMSSW_BASE/src/AZh/combine/figures/azh_2018_btag_mmmt_ZZ_eleES.png`

```
./CheckTemplate.py --analysis azh --year 2017 --cat 0btag --channel eeet --template all --sys all --xmin 200 --xmax 400 --logx --verbosity
```
With this command plots of all MC templates along with all systematic variations (one output png file per template/systematics) will be save in the folder `$CMSSW_BASE/src/AZh/combine/figures`. The x axis will be set to the range [200,400] with log scale. Detailed printout will be activated. The plots will be produced for year `2017`, `eeet` channel in `0btag` category. 

```
./CheckTemplate.py --analysis hig18023 --channel eett --template ggA -mass 300 --sys CMS_scale_t_3prong --xmin 200 --xmax 400 
```
With this commant plots of the ggA template with all systematic variations of uncertainty `CMS_scale_t_3prong` will be produced for datacards of the HIG-18-023 analysis and put in the folder `$CMSSW_BASE/src/AZh/combine/figures`. 

## Running limits

Example below shows how to compute expected limits on the rate of the process ggA, while rate of the bbA process is set to zero. 
```
combine -M AsymptoticLimits -d datacards/Run2/1000/ws.root \ 
--setParameters r_bbA=0,r_ggA=0 \
--setParameterRanges r_ggA=-30,30 \ 
--redefineSignalPOIs r_ggA \
--freezeParameters r_bbA \
--rAbsAcc 0 --rRelAcc 0.0005 \ 
--X-rtd MINIMIZER_analytic \
--cminDefaultMinimizerStrategy 0 \
--cminDefaultMinimizerTolerance 0.01 \ 
--noFitAsimov -t -1 \ 
-n ".azh_Run2_ggA" -m 1000 \
```
In this example, limits are calculated for the combined Run2 analysis and for mass hypothesis of mA = 1000 GeV, implying that workspace is located in folder `datacards/Run2/1000`. The rate of the bbA process is fixed to zero by settings `--setParameters r_bbA=0` and `--freezeParameters r_bbA`. The flags `--noFitAsimov -t -1` instructs combine utility to compute expected limits without fitting signal+background model to data. The flag `-n ".azh_Run2_bbA"` defined the suffix to be assigned to the output root file with the results of limit computation. In this example output root file will be saved under the name `higgsCombine.azh_Run2_ggA.AsymptoticLimits.mH1000.root`. All other parameters steer the fit and limit finding algorithms. One should swap POIs `r_ggA` and `r_bbA` in the command above to compute limit on the rate of bbA process with the rate of ggA fixed to zero. 

To compute limits on the ggA rate while profiling in the fit the rate of bbA process, one has to remove flag  `--freezeParameters r_bbA` and allow parameter `r_bbA` to float freely in a reasonably large range : `--setParameterRanges r_ggA=-30,30:r_bbA=-30,30`. It is suggested to vary POIs within the reasonable range to accelerate computation. Range [-30,30] seems to be reasonable for both r_ggA and r_bbA.

To compute observed limits one needs to remove the flag `--noFitAsimov -t -1`.

Macro [RunLimits.py](https://github.com/raspereza/AZh/blob/main/combine/RunLimits.py) automatises computation of limits with `combine` utility. It is executed with the following parameters:
```
./RunLimits.py --analysis $analysis --year $year --type ${exp,obs} --outdir $outdir --mass $mass
```
where
* `$analysis = {hig18023, azh}` : if set to `hig18023` or `HIG18023` limits are computed for the HIG18-023 analysis, if set to `azh` or `AZh` - limits are computed for the current analysis (default = `azh`);
* `$year = {2016, 2017, 2018, Run2}` (default = `Run2`);
* `$type = {exp,obs} ` : expected to observed limits (default = `exp`);
* `$mass` : mA hypothesis (default = `1000`);
* `$outdir ` : folder where results of limit computation will be stored (the user is required to specify this argument);
For a specified mass limits will be computed for both `r_ggA` and `r_bbA`. To set `r_bbA` to zero when running limits on `r_ggA` and vice versa), add flag `--freezeOtherPOI`. If you wish to compute limits for all mass points, specify `--mass all`. Running limits for all mass points takes some time, be patient. It is advised to run limits for all mass points in screen mode.

## Plotting limits
Limits are plotted by the RooT macro [PlotLimits.C](https://github.com/raspereza/AZh/blob/main/combine/PlotLimits.C) executed with the following arguments:
```
void PlotLimits(
TString Era = "Run2",
TString Process = "bbA",
TString folder = "limits",
TString type = "exp",
float YMax = 10,
float XMin = 225.,
float XMax = 1000.,
bool logx = false,
bool blindData = false) 
```

## Running impacts
It is advised to create separate folder where this step of statistical inference will be carried out and output is stored
```
mkdir impacts
cd impacts
``` 
Impacts of nuisances parameters on the signal strength along with their postfit values are computes by running `combine` with flag `-M Impacts`. In the first step, one performs initial fit and scan of POI (either r_ggA or r_bbA). Example:
```
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/300/ws.root -m 300 --redefineSignalPOIs r_ggA --setParameters r_ggA=1,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-10,10 --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --doInitialFit
```
The combine utility takes as an input combined Run 2 workspace created for mA=300 GeV and performs fit and likelihood scan of r_ggA (rate of ggA is define as POI with argument `--redefineSignalPOIs r_ggA`) using Asimov dataset (flags `-t -1`) built for signal+background model with r_ggA set to 1 and r_bbA set to 0 (`--setParameters r_ggA=1,r_bbA=0`). To perform fit on data remove flags `-t -1`. After the first step, the likelihood scan of all nuisance parameters is performed:
```
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/300/ws.root -m 300 --redefineSignalPOIs r_ggA --setParameters r_ggA=1,r_bbA=0 --setParameterRanges r_ggA=-10,10:r_bbA=-10,10 --robustFit 1 --cminDefaultMinimizerTolerance 0.05 --X-rtd MINIMIZER_analytic --X-rtd FITTER_NEW_CROSSING_ALGO --cminDefaultMinimizerStrategy 1 -t -1 --job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 4 --doFits
```
Again, to perform scans on data one has to remove flags `-t -1`.

Since this procedure is time consuming, the task of running likelihood scan for all parameters is parallelised by submitting jobs to batch system (`--job-mode condor --sub-opts='+JobFlavour = "workday"'`). In the example above each job will perform scan of 4 nuisances parameters (`--merge 4`). Once all jobs are finished, results are collected into json file and summary plot with diagnostis of nuisance parameters (impacts on signal strength r_ggA, postfit values and uncertainties) is create:
```
combineTool.py -M Impacts -d ${CMSSW_BASE}/src/AZh/combine/datacards/Run2/300/ws.root --redefineSignalPOIs r_ggA -m 300 -o impacts.json
plotImpacts.py -i impacts.json -o impacts

```
In the example above, the summary plot will be contained in pdf file `impacts.pdf`.

## Running GoF tests


## Running fits
