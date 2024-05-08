void PrintYields(TString hchannel = "em",
		 TString cat = "0btag",
		 TString year="2016",
		 TString folder="root_files") {
  
  vector<TString> zchannels = {"mm","ee"};

  std::cout << "+++++++++++++++++++++++" << std::endl;
  std::cout << "Year      : " << year << std::endl;
  std::cout << "Folder    : " << folder << std::endl;
  std::cout << "Channel   : " << hchannel << std::endl;
  std::cout << "Category  : " << cat << std::endl;
  std::cout << std::endl;

  map<TString, vector<TString> > backgrounds = {
    {"ZZ       "  , {"ZZ","ggZZ"}},
    {"VVV      "  , {"VVV"}},
    {"Higgs    "  , {"ggHZZ","ZHtt","TTHtt","ZHWW","WHtt"}},
    {"TTV      "  , {"TTW","TTZ"}},
    {"reducible"  , {"reducible"}}};

  map<TString, double> bkg_yields = {
    {"ZZ       ", 0},
    {"VVV      ", 0},
    {"Higgs    ", 0},
    {"TTV      ", 0},
    {"reducible", 0}};

  TFile * file = new TFile(folder+"/MC_data_"+cat+"_"+year+".root");
  for (auto zchannel : zchannels) {
    TString channel = zchannel + hchannel;
    for (auto bkg_yield : bkg_yields) {
      TString name = bkg_yield.first;
      vector<TString> bkg_set = backgrounds[name];
      //      std::cout << name << ":" << bkg_set.size() << std::endl;
      for (auto bkg: bkg_set) {
	TH1D * hist = (TH1D*)file->Get(channel+"/"+bkg);
	//	cout << name << ":" << bkg << ":" << hist->GetSumOfWeights() << std::endl;
	bkg_yields[name] += hist->GetSumOfWeights();
      }
    }
    
  }
  
  std::cout << "OK" << std::endl;

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
  for (auto bkg : backgrounds) {
    TString name = bkg.first;
    double yield = bkg_yields[name];
    total += yield;
    std::cout << name;
    printf(" : %5.3f\n",yield);
  }
  printf("Total : %5.3f\n",total);
  printf("Data  : %4.2f\n",dataYield);
}
