void PrintYields(TString hchannel = "et") {
  
  vector<TString> zchannels = {"mm","ee"};

  map<TString, TString> backgrounds = {
    {"ZZ"         , "ZZ       "},
    {"ggZZ"       , "ggZZ     "},
    {"VVV"        , "VVV      "},
    {"ggHZZ"      , "ggHZZ    "},
    {"ZHtt"       , "ZHtt     "},
    {"TTHtt"      , "TTHtt    "},
    {"ZHWW"       , "ZHWW     "},
    {"WHtt"       , "WHtt     "},
    {"TTW"        , "ttW      "},
    {"TTZ"        , "ttZ      "},
    {"reducible"  , "reducible"}};

  map<TString, double> bkg_yields = {
    {"ZZ"      , 0},
    {"ggZZ"    , 0},
    {"VVV"     , 0},
    {"ggHZZ"   , 0},
    {"TTHtt"   , 0},
    {"ZHtt"    , 0},
    {"ZHWW"    , 0},
    {"WHtt"    , 0},
    {"TTW"     , 0},
    {"TTZ"     , 0},
    {"reducible", 0},
    {"data_obs", 0}};

  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    TFile * file = new TFile("root_files/MC_data_0btag_2016.root");
    for (auto bkg_yield : bkg_yields) {
      TString name = bkg_yield.first;
      TH1D * hist = (TH1D*)file->Get(channel+"/"+name);
      bkg_yields[name] += hist->GetSumOfWeights();
    }
    
  }
  
  TFile * file = new TFile("root_files/signal_300_0btag_2016.root");
  double signalYield = 0;
  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    TH1D * hist = (TH1D*)file->Get(channel+"/ggA");
    signalYield += hist->GetSumOfWeights();
  }

  double total = 0;
  printf("ggA300        : %5.3f\n",signalYield);
  for (auto bkgd : backgrounds) {
    TString name = bkgd.first;
    TString title = bkgd.second;
    double yield = bkg_yields[name];
    total += yield;
    std::cout << title;
    printf(" : %5.3f\n",yield);
  }
  printf("Total : %5.3f\n",total);
  printf("Data  : %4.2f\n",bkg_yields["data_obs"]);
}
