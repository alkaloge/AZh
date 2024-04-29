void PrintYields(TString hchannel = "mt",
		 TString cat = "0btag",
		 TString year="2018",
		 TString folder="root_files") {
  
  vector<TString> zchannels = {"mm","ee"};

  std::cout << "+++++++++++++++++++++++" << std::endl;
  std::cout << "Year      : " << year << std::endl;
  std::cout << "Folder    : " << folder << std::endl;
  std::cout << "Channel   : " << hchannel << std::endl;
  std::cout << "Category  : " << cat << std::endl;
  std::cout << std::endl;

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
    {"reducible", 0}};

  TFile * file = new TFile(folder+"/MC_data_"+cat+"_"+year+".root");
  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    for (auto bkg_yield : bkg_yields) {
      TString name = bkg_yield.first;
      TH1D * hist = (TH1D*)file->Get(channel+"/"+name);
      bkg_yields[name] += hist->GetSumOfWeights();
    }
    
  }
  
  file = new TFile(folder+"/signal_300_"+cat+"_"+year+".root");
  double signalYield = 0;
  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    TH1D * hist = (TH1D*)file->Get(channel+"/ggA");
    signalYield += hist->GetSumOfWeights();
  }
  file = new TFile(folder+"/MC_data_"+cat+"_"+year+".root");
  double dataYield = 0;
  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    TH1D * hist = (TH1D*)file->Get(channel+"/data_obs");
    dataYield += hist->GetSumOfWeights();
  }
  
  double total = 0;
  printf("ggA300    : %5.3f\n",signalYield);
  for (auto bkgd : backgrounds) {
    TString name = bkgd.first;
    TString title = bkgd.second;
    double yield = bkg_yields[name];
    total += yield;
    std::cout << title;
    printf(" : %5.3f\n",yield);
  }
  printf("Total : %5.3f\n",total);
  printf("Data  : %4.2f\n",dataYield);
}
