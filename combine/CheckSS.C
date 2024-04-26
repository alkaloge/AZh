void CheckSS(TString channel = "et") {
  
  TFile * fileOld = new TFile("root_files/reducible_old/"+channel+"_comb_m4l_cons_SS_2018.root");
  TFile * fileNew = new TFile("root_files/reducible_prompt/"+channel+"_comb_m4l_cons_SS_2018.root");

  TH1D * histFFOld = (TH1D*)fileOld->Get("ss_application");
  TH1D * histFFNew = (TH1D*)fileNew->Get("ss_application");

  TH1D * histRedOld = (TH1D*)fileOld->Get("reducible");
  TH1D * histRedNew = (TH1D*)fileNew->Get("reducible");

  TH1D * histDataOld = (TH1D*)fileOld->Get("data");
  TH1D * histDataNew = (TH1D*)fileNew->Get("data");

  double xFFOld = histFFOld->GetSumOfWeights();
  double xFFNew = histFFNew->GetSumOfWeights();

  double xRedOld = histRedOld->GetSumOfWeights();
  double xRedNew = histRedNew->GetSumOfWeights();

  double xDataOld = histDataOld->GetSumOfWeights();
  double xDataNew = histDataNew->GetSumOfWeights();
  
  printf("FF        : %6.3f   %6.3f\n",xFFOld,xFFNew);
  printf("reducible : %6.3f   %6.3f\n",xRedOld,xRedNew);
  printf("data      : %6.3f   %6.3f\n",xDataOld,xDataNew);


}
