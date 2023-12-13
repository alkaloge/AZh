#include "HttStylesNew.cc"
#include "CMS_lumi.C"

void PlotComparison(TString Era = "2016", // year 
		    TString Process = "ggA", // process
		    TString CompareTo = "hig18023", // other options : "2017", "2018"
		    TString folder = "limits", // folder with output of limit computation
		    TString folder2 = "limits_hig18023", // second folder with output of limit computation
		    float YMax = 20,
		    float XMin = 220.,
		    float XMax = 400.,
		    bool blindData = true) {


  std::vector<TString> masses_azh = {"225","275","300","325","350","375","400","450","500","600","700","800","900","1000","1200","1400","1600","1800","2000"};

  std::vector<TString> masses_hig18023 = {"220","240","260","280","300","350","400"};

  std::vector<TString> masses2 = masses_hig18023;
  bool isHIG18023 = true;
  if (CompareTo=="2017"||CompareTo=="2018") {
    masses2 = masses_azh;
    isHIG18023 = false;
    std::cout << "-----------------------------------------" << std::endl;
    //    std::cout << "Comparing " << Era << " and " CompareTo << " for process " << Process << std::endl;
    std::cout << "-----------------------------------------" << std::endl;
    std::cout << std::endl;    

  }
  else if (CompareTo=="hig18023") {
    masses2 = masses_hig18023;
    isHIG18023 = true;
    std::cout << "----------------------------------" << std::endl;
    std::cout << "Comparing to the HIG18-023 analysis" << std::endl;
    std::cout << "-----------------------------------" << std::endl;
    std::cout << std::endl;
  }
  else {
    std::cout << std::endl;
    std::cout << "Unknown option for comparison : " << CompareTo << std::endl;
      
  }

  std::map<TString,TString> lumiLabel = {
    {"Run2","Run 2, 138 fb^{-1}"},
    {"UL_2018","2018, 59.8 fb^{-1}"},
    {"UL_2017","2017, 41.5 fb^{-1}"},
    {"UL_2016","2016, 36.3 fb^{-1}"}
  };

  lumi_13TeV = lumiLabel[Era];

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

  double MH;
  double LIMIT;

  int counter = 0;

  for (auto mass : masses_azh) {

    TString fileName = folder + "/higgsCombine.azh_"+Era+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    std::cout << fileName << std::endl;

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
  for (auto mass : masses2) {
    
    TString fileName = folder2 + "/higgsCombine.azh_"+CompareTo+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    
    if (isHIG18023)
      fileName = folder2 + "/higgsCombine.hig18023_2016_ggA.AsymptoticLimits.mH"+mass+".root";
    
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

  std::cout << " m(A)  -2s   -1s   exp   +1s   +2s   obs " << std::endl; 
  //           "100  24.1  28.2  33.8  40.8  48.2  23.0


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
  std::cout << std::endl;
  std::cout << std::endl;
  std::cout << " m(A)  -2s   -1s   exp   +1s   +2s   obs " << std::endl; 
  //           "100  24.1  28.2  33.8  40.8  48.2  23.0
  for (int i=0; i<counter_H; ++i) {

    char strOut[200];
    sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f",
	    int(mA_H[i]),minus2R_H[i],minus1R_H[i],median_H[i],plus1R_H[i],plus2R_H[i]);
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
  
  int nPointsX = counter;
  int nPointsH = counter_H;

  TGraph * obsG = new TGraph(nPointsX, mA, obs);
  obsG->SetLineWidth(3);
  obsG->SetLineColor(1);
  obsG->SetLineWidth(2);
  obsG->SetMarkerColor(1);
  obsG->SetMarkerStyle(20);
  obsG->SetMarkerSize(1.4);

  TGraph * expH = new TGraph(nPointsH, mA_H, median_H);
  expH->SetLineWidth(3);
  expH->SetLineColor(4);
  expH->SetLineStyle(2);
  expH->SetMarkerSize(0);

  TGraph * expG = new TGraph(nPointsX, mA, median);
  expG->SetLineWidth(3);
  expG->SetLineColor(2);
  expG->SetLineStyle(2);
  

  TGraphAsymmErrors * observed = new TGraphAsymmErrors(nPointsX, mA, central, zeros, zeros, lower, upper);
  observed->SetFillColor(kCyan-4);
  observed->SetLineWidth(3);

  TGraphAsymmErrors * innerBand = new TGraphAsymmErrors(nPointsX, mA, median, zeros, zeros, minus1, plus1);
  innerBand->SetFillColor(kGreen);
  innerBand->SetLineColor(kGreen);

  TGraphAsymmErrors * outerBand = new TGraphAsymmErrors(nPointsX, mA, median, zeros, zeros, minus2, plus2);
  outerBand->SetFillColor(kYellow);
  outerBand->SetLineColor(kYellow);

  TH2F * frame = new TH2F("frame","",2,XMin,XMax,2,0,YMax);
  frame->GetXaxis()->SetTitle("m_{A} (GeV)");
  frame->GetYaxis()->SetTitle("#sigma("+Process+")#timesB(A#rightarrowZh) [fb]");
  frame->GetXaxis()->SetNdivisions(505);
  frame->GetYaxis()->SetNdivisions(206);
  frame->GetYaxis()->SetTitleOffset(1.25);  
  frame->GetYaxis()->SetTitleSize(0.048);  
  

  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);

  frame->Draw();

  //  outerBand->Draw("3same");
  //  innerBand->Draw("3same");
  expG->Draw("lsame");
  expH->Draw("lsame");
  if (!blindData)
    obsG->Draw("lpsame");

  float xLeg = 0.18;
  float yLeg = 0.83;
  float xLegend = 0.57;
  float yLegend = 0.41;
  float sizeLeg = 0.27;

  TLegend * leg = new TLegend(0.40,0.60,0.70,0.80);
  leg->SetFillColor(0);
  leg->SetTextSize(0.035);
  leg->SetBorderSize(0);
  if (!blindData) 
    leg->AddEntry(obsG,"Observed","lp");
  leg->AddEntry(expG,"Expected (this analysis)","l");
  leg->AddEntry(expH,"Expected (HIG-18-023)");
  //  leg->AddEntry(innerBand,"#pm1#sigma Expected","f");
  //  leg->AddEntry(outerBand,"#pm2#sigma Expected","f");
  leg->Draw();

  extraText = "Internal";
  writeExtraText = true;
  CMS_lumi(canv,4,33); 
  canv->RedrawAxis();

  leg->Draw();
  canv->Update();
  //  TString suffix(fileList);
  //  canv->Print("BR_"+suffix+".pdf","Portrait pdf");
  canv->Print("figures/Limits_"+Process+"_"+Era+"_ComparedTo_"+CompareTo+".png");

}
