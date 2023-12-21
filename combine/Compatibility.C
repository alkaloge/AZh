#include "HttStylesNew.cc"

void Compatibility(TString channel = "Run2",
		   TString Algo = "saturated",
		   TString Name = "A#rightarrow Zh#rightarrow (ee+#mu#mu)(#tau#tau) (Run2)",
		   int bins = 60,
		   float xmin = 400,
		   float xmax = 700) {

  SetStyle();
  gStyle->SetOptStat(0);

  //  TFile * fileObs = new TFile("GoF/gof_Closure_"+channel+"_"+Algo+".obs.root");
  TFile * fileObs = new TFile("GoF/gof_Run2_ggA300_obs.root");
  double obs;
  TTree * treeObs = (TTree*)fileObs->Get("limit");
  treeObs->SetBranchAddress("limit",&obs);
  treeObs->GetEntry(0);

  //  TFile * file = new TFile("GoF/gof_Closure_"+channel+"_"+Algo+".exp.root");  
  TFile * file = new TFile("GoF/gof_Run2_ggA300_exp.root");  
  double limit;

  TTree * tree = (TTree*)file->Get("limit");
  tree->SetBranchAddress("limit",&limit);

  TH1F * chi2 = new TH1F("chi2",Name,bins,xmin,xmax);
  TH1F * chi2cut = new TH1F("chi2cut",Name,bins,xmin,xmax);
  InitSignal(chi2);
  chi2->SetLineStyle(1);
  chi2->SetLineWidth(2);

  int entries = tree->GetEntries();
  float count = 0;
  float Entries = 0;
  float xMax = -1;
  float xMin = 1e+10;
  for (int i=0; i<entries; ++i) {
    tree->GetEntry(i);
    chi2->Fill(float(limit));
    Entries += 1.0;
    if (limit>xMax) xMax = limit;
    if (limit<xMin) xMin = limit;
    if (limit>obs) {
      count += 1.0;
      chi2cut->Fill(float(limit));      
    }
  }
  chi2cut->SetFillColor(kCyan);

  std::cout << "Minimal value of q        = " << xMin << std::endl;
  std::cout << "Maximal value of q        = " << xMax << std::endl;
  std::cout << "Observed value of q       = " << obs << std::endl;
  std::cout << "Number of toys with q>obs = " << count << std::endl;
  std::cout << "Total number of toys      = " << entries << std::endl;
  float prob = count / float(Entries);
  std::cout << "p-value                   = " << prob << std::endl;
  char probChar[5];
  sprintf(probChar,"%4.2f",prob);
  TString probStr = TString("p-value = ") + TString(probChar);

  float yMax = 0.6*chi2->GetMaximum();
  float yArrow = 0.05*chi2->GetMaximum();

  chi2->SetNdivisions(505,"X");

  TCanvas * canv = new TCanvas("canv","",700,600);
  if (Algo.Contains("saturated"))
    chi2->GetXaxis()->SetTitle("#chi^{2}");
  if (Algo.Contains("KS"))
    chi2->GetXaxis()->SetTitle("q_{KS}");
  if (Algo.Contains("AD"))
    chi2->GetXaxis()->SetTitle("q_{AD}");
  chi2->GetYaxis()->SetTitle("toys");
  chi2->GetYaxis()->SetTitleOffset(1.2);
  //  chi2->GetYaxis()->SetTitleSize(0.05);
  chi2->GetXaxis()->SetTitleOffset(1.2);
  //  chi2->GetXaxis()->SetTitleSize(0.05);
  chi2->Draw();
  //  chi2cut->Draw("same");
  float arrW = 0.02*(chi2->GetBinLowEdge(bins+1)-chi2->GetBinLowEdge(1));
  TLine * line = new TLine(obs,0,obs,yMax);
  line->SetLineWidth(3);
  line->SetLineColor(4);
  line->Draw();
  TLine * line1 = new TLine(obs,0,obs-arrW,yArrow);
  line1->SetLineWidth(3);
  line1->SetLineColor(4);
  line1->Draw();
  TLine * line2 = new TLine(obs,0,obs+arrW,yArrow);
  line2->SetLineWidth(3);
  line2->SetLineColor(4);
  line2->Draw();  
  TLatex * tex = new TLatex(0.62,0.82,probStr);
  tex->SetNDC();
  tex->SetTextSize(0.050);
  tex->SetLineWidth(2);
  tex->Draw();

  canv->Update();
  canv->Print("gof_"+channel+"_"+Algo+".png");

}
