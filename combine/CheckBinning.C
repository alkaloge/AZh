void CheckBinning() {

  TFile * file = new TFile("root_files/tighten_mtt/MC_0btag_2018.root");
  TH1D * hist = (TH1D*)file->Get("mmmt/ZZ");
  int nbins = hist->GetNbinsX();
  for (int ib=1; ib<=nbins; ++ib) {
    double low = hist->GetBinLowEdge(ib);
    double high = hist->GetBinLowEdge(ib+1);
    printf("%2i : [%4i,%4i]\n",ib,int(low),int(high));
  }

}
