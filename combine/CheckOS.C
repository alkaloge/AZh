void CheckOS(TString channel = "et",
	     TString templ = "ggZZ") {
  
  vector<TString> btags = {"0btag","btag"};
  double reducible_new = 0; 
  for (auto btag : btags) {
    TFile * file = new TFile("root_files/newfakes_bin5GeV/MC_"+btag+"_2018.root");
    TH1D * hist = (TH1D*)file->Get("mm"+channel+"/"+templ);
    reducible_new += hist->GetSumOfWeights();
    hist = (TH1D*)file->Get("ee"+channel+"/"+templ);
    reducible_new += hist->GetSumOfWeights();
  }
  double reducible_old = 0; 
  for (auto btag : btags) {
    TFile * file = new TFile("root_files/tighten_mtt_bin5GeV/MC_"+btag+"_2018.root");
    TH1D * hist = (TH1D*)file->Get("mm"+channel+"/"+templ);
    reducible_old += hist->GetSumOfWeights();
    hist = (TH1D*)file->Get("ee"+channel+"/"+templ);
    reducible_old += hist->GetSumOfWeights();
  }

  printf("reducible : new = %6.3f ; old = %6.3f\n",reducible_new,reducible_old);
  

}
