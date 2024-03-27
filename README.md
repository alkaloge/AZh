# A->Zh->(ll)(tautau) : statistical analysis 

This documentation describes statistical analysis package used in the search for heavy pseudoscalar boson A in the A->Zh->(ee+mm)(tau+tau) decay channel. The search uses ultra-legacy data collected with the CMS detector during Run2 of the CERN Large Hadron Collider in years 2016-2018.

## Installation

The statistical analysis of the A->Zh search results requires [Higgs combination package](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit), [CombineHarvester toolkit](https://cms-analysis.github.io/CombineHarvester/index.html) and [python analysis code](https://github.com/raspereza/AZh.git). We recommend to download also [datacards of the previous analysis HIG-18-023](https://gitlab.cern.ch/cms-analysis/hig/HIG-18-023) for comparison. The code uses as inputs RooT files containing observed and predicted distributions of the final discriminant - 4-lepton mass reconstructed with the FastMTT algorithm, m(4l). Histograms are provided for data, MC background and signal sample, and data-driven background with jets misidentified as leptons. The inputs have been provided by Justin Gage Dezoort. For convenience the RooT files have been moved from the [original repository](https://github.com/GageDeZoort/azh_coffea/tree/main/src/notebooks/for_alexei/tighten_mtt/datacard_templates) to [this repository](https://github.com/raspereza/AZh/tree/main/combine/root_files/coffea).

For the purpose of backtracking of the analysis, it recommended to leave [folder](https://github.com/raspereza/AZh/tree/main/combine/root_files/coffea) intact. Once updated RooT with templates become available create the new folder in the [repository of shapes](https://github.com/raspereza/AZh/tree/main/combine/root_files), for example 'coffea_v2' and copy the new files with the shape there. When running script [Setup.py](https://github.com/raspereza/AZh/blob/main/combine/Setup.py) you should indicate the name of this subfolder as an input argument as described below. 

We advise users of this package to consult documentation of the [Combine package](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit) and [CombineHarvester toolkit](https://cms-analysis.github.io/CombineHarvester/index.html) for detailed information on the statistical methods employed in CMS. 

Installation of the package proceeds as follows:
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_13
cd CMSSW_10_6_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git checkout v8.2.0
cd ../..
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester -b 102x
git clone https://github.com/raspereza/AZh.git AZh
scramv1 b -j 4
```

RooT files with shapes to be used as inputs for datacards producer, are stored in the folder [$CMSSW_BASE/src/AZh/combine/root_files/coffea](https://github.com/raspereza/AZh/tree/main/combine/root_files/coffea). At the stage of setting up environment their copies are place in the folder [$CMSSW_BASE/src/AZh/combine/root_files/backup](https://github.com/raspereza/AZh/tree/main/combine/root_files/backup).

After installation is complete, change to the directory [$CMSSW_BASE/src/AZh/combine](https://github.com/raspereza/AZh/tree/main/combine). All scripts will be run in this directory.

Download datacards of the HIG-18-023 analysis from gitlab repo:
```
cd $CMSSW_BASE/src/AZh/combine
git clone https://gitlab.cern.ch/cms-analysis/hig/HIG-18-023/datacards.git HIG-18-023/datacards
```

Then execute macro [Setup.py](https://github.com/raspereza/AZh/blob/main/combine/Setup.py)
```
./Setup.py --year $year --binning $binning --folder $folder
```
The macro takes the following input arguments:
* `year` : 2016, 2017, 2018, Run2. Default option is `Run2` which will create RooT files for analysis of combined Run2 data.
* `binning` : coarse, nominal, fine. This argument defines binning of templates. Default option is `nominal`. Three options are discussed in presentation at the [Higgs meeting]() on 5/03/2024.
* `folder` : folder where initial RooT files are located. Default: `coffea`. Once you have updated RooT files obtained with coffea framework, create the new folder in `$CMSSW_BASE/src/AZh/combine/root_files`, copy the new files to this folder and specify the name of folder via input argument `--folder`.

The macro performs the following actions :
1. For each year (2016, 2017 and 2018) it merges separate RooT files with data and background templates into one file since [CombineHarvester](https://cms-analysis.github.io/CombineHarvester/index.html) is looking for data distributions and background templates in the same RooT file.
2. It fixes bins with negative content in signal and backgroun templates.
3. It creates in the current directory subfolders `figures` and `jobs` where various plots (png files) and batch job scripts will be placed.
4. The script also rescales MC templates of year 2016 to account for updated (more accurately measured) tau Id scale factors. 
5. Finally the macro rebins templates according to the option `binning`.  

TAU POG has released [updated tau ID scale factors](https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2#Corrections_for_the_DeepTauv2p1) in summer 2023. It turned out that for UL2016 samples new scale factors are about 6% higher than previous ones in wide range of tau pT from 20 up to 100 GeV. To account for this effect MC templates are scaled by 
* 6% in mmet, mmmt, eeet and eemt channels; 
* 12% in eett and mmtt channels.

Templates in eeem and mmem channels are left intact. For UL2017 and UL2018 samples, previous measurements of tau ID efficiency are comparable to the new ones. Therefore nothing is done for UL2017 and UL2018 templates.

## Creation of datacards and workspaces

Datacards are created by macro [make_datacards.py](https://github.com/raspereza/AZh/blob/main/combine/make_datacards.py). It is executed as follows:

```
./make_datacards.py --year $year --btag $btag --mass $mass
```
The required input arguments are:
* `$year : {2016, 2017, 2018}`;
* `$btag : {btag, 0btag}`
* `$mass :` mass hypothesis

Optional input arguments are:
* `--folder :` name of the folder, where datacards are stored. Default : `datacards`. This name is used by default by all macros described in the following
* `--model : {r_ggA,r_bbA,2POI}`. Model which is used in the datacard creation. Default is `2POI`, meaning that the model incorporates two parameters of interest, rate of ggA process and rate of bbA process. Specifying `r_ggA` or `r_bbA` implies model with only one signal, ggA or bbA. The rate of other signal is assumed to be zero.
* `--all_channels` : when this option is specified em channel is included in combination. By default this channel is excluded from combination and datacards for this channel are not produced. 
* `--no_bbb` : when this option is enabled, no bin-by-by MC statistical uncertainties are included in datacards. By default datacards are created with option `* autoMCStats 0` meaning that bin-by-bin MC statistical uncertainties are automatically included into uncertainty model.

Datacards for a given year and mass hypothesis are stored in the folder 
* `$folder/$year/$mass`. 

Also datacards for individual channels are created and saved in folders 
* `$folder/$channel/$mass`, where `$channel={et,mt,tt}`. 

This enables running limits individually for each data taking period and channel.  

Combined Run2 datacards are put in folders 
* `datacards/Run2/$mass`

Datacards can be produced for all years and all mass points in one go by executing script [CreateCards.py](https://github.com/raspereza/AZh/blob/main/combine/CreateCards.py)
```
./CreateCards.py 
```
Optional parameters are:
* `--year` : data taking period (2016, 2017, 2018).
* `--mass` : mass of A. 
* `--model={r_ggA,r_bbA,POI}` Default is `2POI`. 
* `--folder` : folder where datacards are saved. Default is `datacards`.
* `--all_channels` : will create combined cards including em channel. By default this channel is excluded.

Running datacards for all years and mass points may take awhile.

At the next step [RooWorkspaces](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2020/exercise/#d-workspaces) for [multisignal model](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2023/parametric_exercise/#building-the-models) need to be produced. This is done with script [CreateWorkspaces.py](https://github.com/raspereza/AZh/blob/main/combine/CreateWorkspaces.py)
```
./CreateWorkspaces.py --mass $mass 
```
where
* `$mass` : mA (default = 300). One can produce workspaces for all mass points in one go by setting `--mass all` 
Additional (optional) arguments 
* `--folder` specifies folder with cards. Default is `datacards`.
* `--batch` flag can be used to send jobs to the condor batch system. One job per mass point will be submited, which will accelerate the task of creating workspaces. 

For each $year and $mass, workspaces are put in the folder `$folder/$year($channel)/$mass` under the name `ws.root`. Workspaces for Run2 combination are put in folders `datacards/Run2/$mass` under the same name. Workspaces are also created for individual channels : `$folder/$channel/$mass/ws.root`, where `--channel={et,mt,tt}`.

Signal model includes two  parameters of interest (POI): rate of the process ggA (r_ggA) and rate of the process bbA (r_bbA). 

Running workspaces for all masses interactively is time consuming, especially for combined Run2 datacards. Therefore it is recommended to submit jobs to the batch system by raising flag `--batch`, for example
```
./CreateWorkspaces.py --mass all --batch
```

## Creating workspaces for HIG18-023 analysis 

To enable comparison with the published HIG-18-023 analysis, corresponding datacards and workspaces need to be also created. It is done using bash script [CombineCards_HIG18023.bash](https://github.com/raspereza/AZh/blob/main/combine/CombineCards_HIG18023.bash). Workspaces for the HIG-18-023 analysis will be put in folders `HIG-18-023/$mass`.

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
With this command plots of the ggA template with all systematic variations of uncertainty `CMS_scale_t_3prong` will be produced for datacards of the HIG-18-023 analysis and put in the folder `$CMSSW_BASE/src/AZh/combine/figures`. 

## Plotting mass distributions from datacards
The distributions of 4-lepton mass can be plotted from created datacards using macro [PlotCards.py](https://github.com/raspereza/AZh/blob/main/combine/PlotCards.py)

```
./PlotCards.py --year $year --channel $channel --cat $cat --mass $mass
```
Inputs :
* `$year={2016,2017,2018,all}` : data-taking period or all data-taking periods combined. 
* `$channel={et,mt,tt,all}` specifies channel (et, mt, tt) or plot combination of channels (all).
* `$cat={0btag,btag,all}` specifies category (btag, 0btag) or plot combination of both.
* `$mass` : mA.

Additional (optional) inputs:
* `--folder` : folder with datacards. Default is `datacards`. 
* `--xmin` : minimal edge of X-axis. Default is 200. 
* `--xmax` : maximal edge of X-axis. Default is 2500.
* `--logx` : logarithmic scale for X-axis.
* `--unblind` : unblind data in plots.

The output plot will be saved in the folder `figures`.`figures/m4l_$year_$cat_$channel_$mass_cards.png`

## Running limits

Example below shows how to compute [Asymptotic](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2020/exercise/#a-asymptotic-limits) expected limits on the rate of the process ggA, while rate of the bbA process is set to zero. 
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
./RunLimits.py --analysis $analysis --sample $sample --outdir $outdir --mass $mass
```
where required inputs are: 
* `$sample = {2016, 2017, 2018, Run2, et, mt, tt}` : year, channel or Run2 combination.
* `$mass` : mA hypothesis (default = `300`). When `--mass all` is specified, limits are computed for all massses.
* `$outdir ` : folder where results of limit computation will be stored.

Optional arguments are:
* `--folder` : folder with datacards (default `datacards`).
* `--obs` : observed limits are computed.
* `--releaseOtherPOI` : limits are computed on ggA (bbA) rates with rate of other process allowed to float freely.


For a specified mass limits will be computed for both `r_ggA` and `r_bbA`. To set `r_bbA` to zero when running limits on `r_ggA` and vice versa), add flag `--freezeOtherPOI`. If you wish to compute limits for all mass points, specify `--mass all`. 
Computation of observed limits is activated with flag `--obs`. Results of computation (asymptotic median limit, 2.5, 16, 84 and 97.5% quantiles, and observed limit ) for a given `$mass` and `$year` and process `$proc={ggA,bbA}` are save in folder `$outdir` in the file named `higgsCombine.azh_${year}_${proc}.AsymptoticLimits.mH${mass}.root`.

It is recommended to save expected and observed limits in different output folders, otherwise results of computation will be overwritten. Limits for different years and for Run 2 combination can be safely 
Running limits for all mass points takes some time. Computation can be accelerated by parallelising the task with flag `--batch`. In this case one job per mass point will be sent to condor batch system.  


## Plotting limits
Once limits are computed they can be plotted as a function of mA using the RooT macro [PlotLimits.C](https://github.com/raspereza/AZh/blob/main/combine/PlotLimits.C). It is executed with the following arguments:
```
void PlotLimits(
TString Era = "Run2", // year
TString Sample = "Run2", // available options : 2016, 2017, 2018, Run2, et, mt, tt
TString Process = "bbA", // process
TString folder = "limits", // folder containing output of the macro RunLimits.py (parameter `--outdir`)
float YMax = 10, // upper boundary of Y axis
float XMin = 225., // lower boundary of X axis
float XMax = 2000., // upper boundary of X axis
bool logx = false, // log scale
bool blindData = true // blinding observed limit
) 
```

## Running impacts

It is advised to create separate folder where this step of statistical inference will be carried out and output is stored, for example
```
mkdir impacts_ggA300
cd impacts_ggA300
``` 

[Impacts](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/tutorial2023/parametric_exercise/#impacts) of nuisances parameters on the signal strength along with their postfit values are computes by running `combine` utility with flag `-M Impacts`. In the first step, one performs initial fit and scan of POI (either r_ggA or r_bbA). Example:
```
combineTool.py -M Impacts -d datacards/Run2/300/ws.root \ 
--redefineSignalPOIs r_ggA \
--setParameters r_ggA=1,r_bbA=0 \
--setParameterRanges r_ggA=-10,10:r_bbA=-10,10 \
--robustFit 1 \
--cminDefaultMinimizerTolerance 0.05 \
--X-rtd MINIMIZER_analytic \
--X-rtd FITTER_NEW_CROSSING_ALGO \
--cminDefaultMinimizerStrategy 1 \
-m 300 \
-t -1 \
--doInitialFit
```
The combine utility takes as an input combined Run 2 workspace created for mA=300 GeV and performs fit and likelihood scan of r_ggA (rate of ggA is define as POI with argument `--redefineSignalPOIs r_ggA`) using Asimov dataset (flags `-t -1`) built for signal+background model with r_ggA set to 1 and r_bbA set to 0 (`--setParameters r_ggA=1,r_bbA=0`). To perform fit on data remove flags `-t -1`. After the first step, the likelihood scan of all nuisance parameters is performed:
```
combineTool.py -M Impacts \
-d datacards/Run2/300/ws.root \
--redefineSignalPOIs r_ggA \
--setParameters r_ggA=1,r_bbA=0 \
--setParameterRanges r_ggA=-10,10:r_bbA=-10,10 \
--robustFit 1 \
--cminDefaultMinimizerTolerance 0.05 \
--X-rtd MINIMIZER_analytic \
--X-rtd FITTER_NEW_CROSSING_ALGO \
--cminDefaultMinimizerStrategy 1 \
-t -1 \
-m 300 \
--job-mode condor --sub-opts='+JobFlavour = "workday"' --merge 4 \
--doFits
```
Again, to perform scans on data, one has to remove flags `-t -1`.

Since this procedure is time consuming, the task of running likelihood scan for all parameters is parallelised by submitting jobs to batch system (`--job-mode condor --sub-opts='+JobFlavour = "workday"'`). In the example above each job will perform scan of 4 nuisances parameters (`--merge 4`). Once all jobs are finished, results are collected into json file and summary plot with diagnostis of nuisance parameters (impacts on signal strength r_ggA, postfit values and uncertainties) is create:
```
combineTool.py -M Impacts -d datacards/Run2/300/ws.root \ 
--redefineSignalPOIs r_ggA -m 300 -o impacts.json \

plotImpacts.py -i impacts.json -o impacts
```
In the example above, the summary plot will be contained in pdf file `impacts.pdf`.

Running impacts for Run 2 combination is automatised with the macro [RunImpacts.py](https://github.com/raspereza/AZh/blob/main/combine/RunImpacts.py):
```
./RunImpacts.py --proc $proc --mass $mass
```
* `$proc` defines process (either ggA or bbA), whose rate will be regarded as POI
* `$mass` - mA 
* 

These two parameters are required to be set by user. By default expected impacts are computed based on the Asimov dataset. In this case one can optionally specify signal strenghts for ggA and bbA processes with flags `--r_ggA ` (default is 1) and `--r_bbA` (default is 0). The script automatically parallelises computation by submitting jobs to the condor batch system. One job performs scan of 4 nuisance parameters. Results of the computation will be stored in the folder `impacts_${proc}${mass}_exp`. For example running script as
```
./RunImpacts.py --proc ggA --mass 300 --r_ggA 2 --r_bbA 0
```
will compute expected impacts on the signal strength of ggA. Computation will assume Asimov dataset with signal strength modifiers of 2 and 0 for the ggA and bbA processes, respectively. Results will be stored in folder `impacts_ggA300_exp`. If you wish to compute impacts on data, set flag `--obs`, for example
```
./RunImpacts.py --proc ggA --mass 300 --r_ggA 2 --r_bbA 0 --obs
```
In this case results will be stored in folder `impacts_ggA300_obs`. 

Once all jobs computing impacts are finished (monitor condor dashboard), results of likelihood scans can be collected and impact plot can be created with macro [PlotImpacts.py](https://github.com/raspereza/AZh/blob/main/combine/PlotImpacts.py). Few examples are given below.

```
./PlotImpacts.py --proc ggA --mass 300
```
With this command pdf file `impacts_ggA300_exp/impacts_ggA300_exp.pdf` will be created using output of running expected impacts on the ggA300 signal strength. Usually impacts of r_ggA (r_bbA) on r_bbA (r_ggA) overwhelms impacts of all other nuisances. Additional pdf `impacts_ggA300_exp/impacts_OnePOI_ggA300_exp.pdf`, where impact of the rate of unconstrained rate parameter on POI is not shown. This makes more visible impacts of other nuisances. 

```
./PlotImpacts.py --proc	ggA --mass 300 --obs
```
This command will create pdf file `impacts_ggA300_exp/impacts_ggA300_obs.pdf` based on the results of computed observed impacts on the ggA300 signal strength. Additional pdf file `impacts_ggA300_exp/impacts_OnePOI_ggA300_obs.pdf` is created without showing impact of other POI (r_bbA) on rate of the ggA process.

The observed fitted value of the signal strength will be hidden in the plot. To unblind signal strength, raise flag `--unblind`
```
./PlotImpacts.py --proc ggA --mass 300 --obs --unblind
```

## Running GoF tests

It is advised to run all the scripts to perform [goodness-of-fit (GoF) test](http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#goodness-of-fit-tests) in separate newly created folder, e.g. 
```
mkdir GoF
cd GoF
```
The GoF test is done in two steps. First, test-statistics is computed in data using [one of three options](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#goodness-of-fit-tests):
* [saturated](https://www.physics.ucla.edu/~cousins/stats/cousins_saturated.pdf);
* Kolmogorov-Smirnov (KS);
* Anderson-Darling (AD).

In the following we will use the saturated, which is frequently used in CMS. Example below illustrates, how one computes test-statistics in data, when probing signal hypothesis with rates 1 and 0 for ggA300 and bbA300 signals, respectively
```
combineTool.py -M GoodnessOfFit \
-d datacards/Run2/300/ws.root \ 
--setParameters r_ggA=1,r_bbA=0 \
-m 300 \ 
--algo saturated \ 
-n .obs
```
If you wish to proble background-only hypothesis, set both signal strengths to zero : `--setParameters r_ggA=0,r_bbA=0`.

The command above will create RooT file `higgsCombine.obs.GoodnessOfFit.mH300.root`, containing tree named `limit`. The tree has only one entry, and the tree brach `limit` stores the computed value of saturated test-statistics in data. 

Afterwards, ensemble of toys is generated under assumption of the signal+packground hypothesis. The sampling is performed given background and signal predictions in each analysis bin and underlying uncertainty model. 
```
combineTool.py -M GoodnessOfFit \ 
-d $CMSSW_BASE/src/AZh/combine/datacards/Run2/300/ws.root --toysFreq \ 
--setParameters r_ggA=1,r_bbA=0 \
-m 300 --algo saturated -n .exp \
-t 1000 
```

The command above will start generating 1000 of toys interactively. But this may take very long time, therefore it is recommended to parallelise task by submitting jobs to the condor batch system, as illustrated below 
```
#!/bash
for i in {1..100}
do
    random=$RANDOM
    echo random seed $random
    combineTool.py -M GoodnessOfFit \ 
    -d $CMSSW_BASE/src/AZh/combine/datacards/Run2/300/ws.root --toysFreq \ 
    --setParameters r_ggA=1,r_bbA=0 \
    -m 300 --algo saturated -n .exp \
    -t 10 \
    --job-mode condor --task-name gof.${random} \
    --sub-opts='+JobFlavour = "workday"' 
done
cd -
```
This bash script will submit 100 jobs to the condor batch system. Each job will produce 10 toys using as a seed random number (`${random}`) generated by operational system, and create RooT file named `higgsCombine.exp.GoodnessOfFit.mH300.${random}.root`. You can use the script [RunGoF.bash](https://github.com/raspereza/AZh/blob/main/combine/RunGoF.bash) as an example for computation of test-statistics in data and generation of toys in one go.    

Once jobs are finished, one can collect results in the folder, where RooT files are stored. 
```
cd GoF
hadd gof_exp.root higgsCombine.exp.GoodnessOfFit.mH300.*.root
mv higgsCombine.obs.GoodnessOfFit.mH300.root gof_obs.root
cd ../
```

The script [Hadd_GoF.bash](https://github.com/raspereza/AZh/blob/main/combine/Hadd_GoF.bash) is intended to collect outputs of GoF test into files with observed test-statistics 


The histogram of test-statistics in ensemble of toys is then compared with the value of test-statistics in data and p-value, quantifying compatibility of data with the model, is computed as integral in the distribution of toys from the actual observed value up to infinity. RooT macro [Compatibility.C](https://github.com/raspereza/AZh/blob/main/combine/Compatibility.C) visualises the procedure
```
void Compatibility(
     TString folder = "GoF_Run2_mA300", // folder with RooT files
     TString Algo = "saturated", // algorithm
     TString legend = "A#rightarrow Zh (Run2)", // legend
     int bins = 60 // number of bins in the histogram of toys
     ) {
```

## Fitting

Example of running maximum likelihood fit can be foung in [RunFit.bash](https://github.com/raspereza/AZh/blob/main/combine/RunFit.bash). The procedure is automated with the python macro [RunFit.py](https://github.com/raspereza/AZh/blob/main/combine/RunFit.py):
```
./RunFit.py --sample $sample --mass $mass
```
Inputs are:
* `$sample={2016,2017,2018,Run2,et,mt,tt}`. Sample to fit. It could be either year, channel or combination 
* `$mass` : mA

Optional inputs are
* `--obs` : activates fir of data (by default Asimov dataset is fitted).
* `--r_ggA` : signal modifier for ggA process. Relevant only if Asimov dataset is fitted. Default = 0.
* `--r_bbA` : signal modifier for bbA process. Relevant	only if	Asimov dataset is fitted. Default = 0.
* `--folder` : folder with datacards. Default is `datacards`.
* `--saveShapes` : ATTENTION! with this flag postfit shapes will be stored. These shapes are used for plotting postfit distributions.
* `--robustHesse` : robustHesse option is activated (improved covariance matrix estimate). By default robustFit option is used (estimate of errors with likelihood scans) 
* `--mininizer` : analytic minimizer option. The fit is sensitive to this parameter. Default option is 1. But one may to try option 0, if fit doesn't converge or yields invalid Hessian matrix. 
* `--batch` : submits job to condor. 

The script performs fit and saves output RooT file in the newly created folder: 
* `fit_$sample_mA$mass_exp/fitDiagnosticsTest.root`, when fit is performed on Asimov dataset
* `fit_$sample_mA$mass_obs/fitDiagnosticsTest.root`, when fit is performed on data

ATTENTION. To save postfit shapes, set flag `--saveShapes`. With this flag fit will run much slower, and may take half a day. Therefore, in this case it is recommended to submit job to condor by setting flag `--batch`. It makes sense to save shapes only when running on data.

## Plotting prefit and postfit distributions
To plot postfit disctribution you have first to run [RunFit.py](https://github.com/raspereza/AZh/blob/main/combine/RunFit.py) with flags `--obs` and `--saveShapes`, and it is recommended to submit job to condor with flag `--batch`. The output of this macro is used to plot postifit distributions. Plotting is done with script [PlotFit.py](https://github.com/raspereza/AZh/blob/main/combine/PlotFit.py):
```
./PlotFit.py --year $year --channel $channel --cat $cat --mass $mass --fittype $fittype
```
* `$year={2016,2017,2018,all}`
* `$channel={et,mt,tt,all}`
* `$cat={btag,0btag,all}`
* `$mass` : mA
* `$fittype={prefit,fit_b,fit_s}` : (prefit, background-only fit, signal fit)

Optional arguments:
* `--xmin` : lower boundary of X-axis (default = 200).
* `--xmax` : upper boundary of X-axis (default = 2500).
* `--logx` : when this flag is set, X-axis is shown in logarithmic scale.
* `--unblind` : when this flag is set, data is unblinded.

The creates plot of the m(4l) distribution and saves plot in the png file `figures/m4l_$year_$cat_$channel_$mass_$fittype.png`. Please note that macro access binning of mass distribution from datacards. Therefore an option is offered to specify the folder with datacards with input parameter `--folder $folder` (default is `datacards`).   

## Closure test of the reducible background 

Validation of reducible background is performed in the sideband region with same-sign tau-lepton candidates. Validation is based on GoF test performed on background templates and data distributions in this sideband region. To enhance statistics btag and 0btag categories, as well Z->ee and Z->mumu decays are combined into one distribution per di-tau channel and year. In total 9 separate distributions are considered in the test : 3 decay modes of tau pairs (em, et, mt and tt) x 3 data-taking periods    

Datacards for validation are produced with the python script [MakeClosureCards.py](https://github.com/raspereza/AZh/blob/main/combine/MakeClosureCards.py). It will make directory  $CMSSW_BASE/src/AZh/combine/ClosureTest, where various subfolders will be created to store datacards for individial data taking periods (2016, 2017, 2018) and di-tau modes (em, et, mt and tt). The combined Run2 workspaces are put in subfolder Run2. The macro will also plot distributions of m(4l) in the SS sideband for individual channels combining Run2 data. The plots are output in files `SS_closure_${channel}_Run2.png`, where `$channel={et, mt, tt}`. 

The GoF tests can be done with the bash script [RunGoF_Closure.bash](https://github.com/raspereza/AZh/blob/main/combine/RunGoF_Closure.bash)
```
./RunGoF_Closure.bash ${argument}
```
where single argument passed to the script is either era (2016, 2017, 2018, Run2) or channel (em, et, mt or tt). 
Examples of running:
``` 
./RunGoF_Closure.bash 2016
```
for specific era or
```
./RunGoF_Closure.bash et
```
for specific channel or
```
./RunGoF_Closure.bash Run2
```
for Run2 combination

The output RooT files are saved in the folder `GoF_ClosureTest_${argument}`, where `${argument}` is single argument passed to the script. Once jobs are finished, one should collect output of the script, e.g.
```
cd GoF_ClosureTest_Run2
cp higgsCombine.obs.GoodnessOfFit.mH300.root gof_obs.root
hadd gof_exp.root higgsCombine.exp.GoodnessOfFit*root
```

The RooT macro [Compatibility.C](https://github.com/raspereza/AZh/blob/main/combine/Compatibility.C) can be used at the end to plot results of GoF test.
 

