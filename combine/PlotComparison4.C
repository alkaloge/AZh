#include "HttStylesNew.cc"
#include "CMS_lumi.C"

void PlotComparison4(TString Era1 = "Run2", // year2 
		     TString Era2 = "Run2", // year2
		     TString Era3 = "Run2", // 
		     TString Era4 = "Run2", // 
		     TString Process = "bbA", // process
		     TString folder1 = "limits_et", // first folder 
		     TString folder2 = "limits_mt", // second folder 
		     TString folder3 = "limits_tt", // 
		     TString folder4 = "limits_em", // 
		     TString leg1 = "#tau_{e}#tau_{h}",
		     TString leg2 = "#tau_{#mu}#tau_{h}",
		     TString leg3 = "#tau_{h}#tau_{h}",
		     TString leg4 = "#tau_{e}#tau_{#mu}",
		     TString postfix = "channels",
		     float YMax = 20, // maximum of Y axis
		     float XMin = 225., // minimum of X axis
		     float XMax = 2000., // maximum of X axis
		     bool blindData = true) {


  std::vector<TString> masses = {"225","250","275","300","325","350","375","400","450","500","600","700","800","900","1000","1200","1400","1600","1800","2000"};

  std::map<TString,TString> lumiLabel = {
    {"Run2","Run 2, 138 fb^{-1}"},
    {"2018","2018, 59.8 fb^{-1}"},
    {"2017","2017, 41.5 fb^{-1}"},
    {"2016","2016, 36.3 fb^{-1}"}
  };

  lumi_13TeV = lumiLabel[Era1];

  float scale = 1;

  SetStyle();
  gStyle->SetOptFit(0000);
  gStyle->SetErrorX(0.5);

  const int nPoints = 20;

  // signal strength limits sigma*BR / sigma*BR (at tanb=30)
  double mA[nPoints];      
  double minus2R[nPoints]; 
  double minus1R[nPoints]; 
  double medianR[nPoints]; 
  double plus1R[nPoints];  
  double plus2R[nPoints];  
  double obsR[nPoints];    

  double obs[nPoints];
  double minus2[nPoints];
  double minus1[nPoints];
  double median[nPoints];
  double plus1[nPoints];
  double plus2[nPoints];

  double minus2R_H[nPoints];
  double minus1R_H[nPoints];
  double median_H[nPoints];
  double plus2R_H[nPoints];
  double plus1R_H[nPoints];
  double mA_H[nPoints];

  double minus2R_G[nPoints];
  double minus1R_G[nPoints];
  double median_G[nPoints];
  double plus2R_G[nPoints];
  double plus1R_G[nPoints];
  double mA_G[nPoints];

  double minus2R_L[nPoints];
  double minus1R_L[nPoints];
  double median_L[nPoints];
  double plus2R_L[nPoints];
  double plus1R_L[nPoints];
  double mA_L[nPoints];

  double minus2R_M[nPoints];
  double minus1R_M[nPoints];
  double median_M[nPoints];
  double plus2R_M[nPoints];
  double plus1R_M[nPoints];
  double mA_M[nPoints];

  double MH;
  double LIMIT;

  int counter = 0;

  for (auto mass : masses) {

    TString fileName = folder1 + "/higgsCombine.azh_"+Era1+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    //    std::cout << fileName << std::endl;

    TFile * file = new TFile(fileName);
    if (file==NULL||file->IsZombie()) {
      std::cout << "file " << fileName << " does not exist... quitting" << std::endl;
      return;
    }


    TTree * tree = (TTree*)file->Get("limit");

    //    std::cout << "file : " << file << std::endl;
    //    std::cout << "tree : " << tree << std::endl;

    tree->SetBranchAddress("limit",&LIMIT);
    tree->SetBranchAddress("mh",&MH);

    tree->GetEntry(0);
    mA[counter] = float(MH);
    minus2R[counter] = scale*float(LIMIT);

    //    std::cout << mA[counter] << std::endl;
    
    tree->GetEntry(1);
    minus1R[counter] = scale*float(LIMIT);

    tree->GetEntry(2);
    medianR[counter] = scale*float(LIMIT);

    tree->GetEntry(3);
    plus1R[counter] = scale*float(LIMIT);

    tree->GetEntry(4);
    plus2R[counter] = scale*float(LIMIT);

    tree->GetEntry(5);
    obsR[counter] = scale*float(LIMIT);
    if (blindData)
      obsR[counter] = scale*medianR[counter];

    counter++; 
      
  }

  int counter_H = 0;
  std::cout << std::endl;

  for (auto mass : masses) {
    
    TString fileName = folder2 + "/higgsCombine.azh_"+Era2+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    
    TFile * file = new TFile(fileName);
    if (file==NULL||file->IsZombie()) {
      std::cout << "file " << fileName << " does not exist... quitting" << std::endl;
      return;
    }

    TTree * tree = (TTree*)file->Get("limit");

    //    std::cout << "file : " << file << std::endl;
    //    std::cout << "tree : " << tree << std::endl;

    tree->SetBranchAddress("limit",&LIMIT);
    tree->SetBranchAddress("mh",&MH);

    tree->GetEntry(0);
    minus2R_H[counter_H] = scale*float(LIMIT);
    
    tree->GetEntry(1);
    minus1R_H[counter_H] = scale*float(LIMIT);

    tree->GetEntry(2);
    mA_H[counter_H] = float(MH);
    median_H[counter_H] = scale*float(LIMIT);

    tree->GetEntry(3);
    plus1R_H[counter_H] = scale*float(LIMIT);
    
    tree->GetEntry(4);
    plus2R_H[counter_H] = scale*float(LIMIT);

    counter_H++;

  }

  int counter_L = 0;
  std::cout << std::endl;

  for (auto mass : masses) {
    
    TString fileName = folder3 + "/higgsCombine.azh_"+Era3+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    
    TFile * file = new TFile(fileName);
    if (file==NULL||file->IsZombie()) {
      std::cout << "file " << fileName << " does not exist... quitting" << std::endl;
      return;
    }

    TTree * tree = (TTree*)file->Get("limit");

    //    std::cout << "file : " << file << std::endl;
    //    std::cout << "tree : " << tree << std::endl;

    tree->SetBranchAddress("limit",&LIMIT);
    tree->SetBranchAddress("mh",&MH);

    tree->GetEntry(0);
    minus2R_L[counter_L] = scale*float(LIMIT);
    
    tree->GetEntry(1);
    minus1R_L[counter_L] = scale*float(LIMIT);

    tree->GetEntry(2);
    mA_L[counter_L] = float(MH);
    median_L[counter_L] = scale*float(LIMIT);

    tree->GetEntry(3);
    plus1R_L[counter_L] = scale*float(LIMIT);
    
    tree->GetEntry(4);
    plus2R_L[counter_L] = scale*float(LIMIT);

    counter_L++;

  }

  int counter_M = 0;
  std::cout << std::endl;

  for (auto mass : masses) {
    
    TString fileName = folder4 + "/higgsCombine.azh_"+Era4+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    
    TFile * file = new TFile(fileName);
    if (file==NULL||file->IsZombie()) {
      std::cout << "file " << fileName << " does not exist... quitting" << std::endl;
      return;
    }

    TTree * tree = (TTree*)file->Get("limit");

    //    std::cout << "file : " << file << std::endl;
    //    std::cout << "tree : " << tree << std::endl;

    tree->SetBranchAddress("limit",&LIMIT);
    tree->SetBranchAddress("mh",&MH);

    tree->GetEntry(0);
    minus2R_M[counter_M] = scale*float(LIMIT);
    
    tree->GetEntry(1);
    minus1R_M[counter_M] = scale*float(LIMIT);

    tree->GetEntry(2);
    mA_M[counter_M] = float(MH);
    median_M[counter_M] = scale*float(LIMIT);

    tree->GetEntry(3);
    plus1R_M[counter_M] = scale*float(LIMIT);
    
    tree->GetEntry(4);
    plus2R_M[counter_M] = scale*float(LIMIT);

    counter_M++;

  }

  std::cout << " m(A)  -2s   -1s   exp   +1s   +2s   obs " << std::endl; 

  for (int i=0; i<counter; ++i) {

    obs[i]    = obsR[i];
    minus2[i] = minus2R[i];
    minus1[i] = minus1R[i];
    median[i] = medianR[i];
    plus1[i]  = plus1R[i];
    plus2[i]  = plus2R[i];

    char strOut[200];
    sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f",
	    int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i]);
    std::cout << strOut << std::endl;

  }

  double zeros[nPoints];
  double upper[nPoints];
  double lower[nPoints];
  double central[nPoints];
  for (int i=0; i<counter; ++i) {
    zeros[i] = 0;
    central[i] = 15; 
    minus2[i] = median[i] - minus2[i];
    minus1[i] = median[i] - minus1[i];
    plus1[i]  = plus1[i]  - median[i];
    plus2[i]  = plus2[i]  - median[i];
    upper[i] = 15 - central[i];
    lower[i] = central[i] - obs[i];
  }
  
  int nPointsG = counter;
  int nPointsH = counter_H;
  int nPointsL = counter_L;
  int nPointsM = counter_M;

  TGraph * expH = new TGraph(nPointsH, mA_H, median_H);
  expH->SetLineWidth(3);
  expH->SetLineColor(4);
  expH->SetLineStyle(1);
  expH->SetMarkerSize(0);

  TGraph * expG = new TGraph(nPointsG, mA, median);
  expG->SetLineWidth(3);
  expG->SetLineColor(2);
  expG->SetLineStyle(1);
  expG->SetMarkerSize(0);
  
  TGraph * expL = new TGraph(nPointsL, mA_L, median_L);
  expL->SetLineWidth(3);
  expL->SetLineColor(1);
  expL->SetLineStyle(1);
  expL->SetMarkerSize(0);

  TGraph * expM = new TGraph(nPointsM, mA_M, median_M);
  expM->SetLineWidth(3);
  expM->SetLineColor(kGreen+2);
  expM->SetLineStyle(1);
  expM->SetMarkerSize(0);

  TH2F * frame = new TH2F("frame","",2,XMin,XMax,2,0,YMax);
  frame->GetXaxis()->SetTitle("m_{A} (GeV)");
  frame->GetYaxis()->SetTitle("#sigma("+Process+")#timesB(A#rightarrowZh) [fb]");
  frame->GetXaxis()->SetNdivisions(505);
  frame->GetYaxis()->SetNdivisions(206);
  frame->GetYaxis()->SetTitleOffset(1.25);  
  frame->GetYaxis()->SetTitleSize(0.048);  

  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);

  frame->Draw();
  expG->Draw("lsame");
  expH->Draw("lsame");
  expL->Draw("lsame");
  expM->Draw("lsame");

  float xLeg = 0.18;
  float yLeg = 0.83;
  float xLegend = 0.57;
  float yLegend = 0.41;
  float sizeLeg = 0.27;

  TLegend * leg = new TLegend(0.45,0.5,0.60,0.80);
  leg->SetFillColor(0);
  leg->SetTextSize(0.05);
  leg->SetBorderSize(0);
  leg->AddEntry(expG,leg1,"l");
  leg->AddEntry(expH,leg2,"l");
  leg->AddEntry(expL,leg3,"l");
  leg->AddEntry(expM,leg4,"l");
  leg->Draw();

  extraText = "Internal";
  writeExtraText = true;
  CMS_lumi(canv,4,33); 
  canv->RedrawAxis();

  leg->Draw();
  canv->Update();
  canv->Print("figures/Limits_"+Process+"_"+Era1+"_"+postfix+".png");

}
