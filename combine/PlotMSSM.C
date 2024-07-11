#include "HttStylesNew.cc"
#include "CMS_lumi.C"

float interpolate(int npoints, float * tanb, float * r) {

  int i1 = 0;
  int i2 = 1;

  if (r[0]>1.0) {
    i1 = 0;
    i2 = 1;
  }
  else if (r[npoints-1]<1.0) {
    i1 = npoints-2;
    i2 = npoints-1;
  }
  else {
    for (int i=1; i<npoints-1; ++i) {
      if (r[i-1]<1.0&&r[i]>1.0) {
	i1 = i-1;
	i2 = i;
      }
    }
  }
  // tanb[i1] = a + b*r[i1]
  // tanb[i2] = a + b*r[i2] 
  // b = (tanb[i2]-tanb[i1])/(r[i2]-r[i1])
  // a = tanb[i1] - b*r[i1]
  // tanb = a + b

  float b = (tanb[i2]-tanb[i1])/(r[i2]-r[i1]);
  float a = tanb[i1] - b*r[i1];
  
  return a+b;

}

void PlotMSSM(TString model = "mh125EFT_13",
	      float YMin = 0.9999, // lower boundary of Y axis
	      float YMax = 6.00001, // upper boundary of Y axis
	      float XMin = 225., // lower boundary of X axis
	      float XMax = 400., // upper boundary of X axis
	      bool logx = false, // log scale of X axis
	      bool logy = true, // log scale of Y axis
	      bool blindData = false // blinding observed limit
	      ) {


  std::vector<TString> masses = {"225","250","275","300","325","350","375","400"};  

  float tanb_min = 1.0;
  float tanb_max = 7.0;
  float dtanb = 0.1;

  TString Title("hMSSM");
  if (model=="hMSSM_13") {
    Title = "hMSSM scenario";
    dtanb = 0.2;
  }
  else if (model=="mh125EFT_13") {
    Title = "M_{h,EFT}^{125} scenario";
    dtanb = 0.25;
  }

  lumi_13TeV = "138 fb^{-1}";
  TString folder = "models/"+model;

  SetStyle();
  gStyle->SetOptFit(0000);
  gStyle->SetErrorX(0.5);

  const int nPoints = 20;

  // signal strength limits sigma*BR / sigma*BR (at tanb=30)
  float mA[nPoints];      
  float minus2R[nPoints]; 
  float minus1R[nPoints]; 
  float medianR[nPoints]; 
  float plus1R[nPoints];  
  float plus2R[nPoints];  
  float obsR[nPoints];    

  float obs[nPoints];
  float minus2[nPoints];
  float minus1[nPoints];
  float median[nPoints];
  float plus1[nPoints];
  float plus2[nPoints];

  double MH;
  double LIMIT;

  int counter = 0;
  for (auto mass : masses) {
    
    int counter_tb = 0;
    float tanb = tanb_min;
    float tanb_v[100];
    float obs_v[100];
    float median_v[100];
    float minus1_v[100];
    float minus2_v[100];
    float plus1_v[100];
    float plus2_v[100];
    while (tanb<=tanb_max) {

	char tanb_str[20];
	sprintf(tanb_str,"%4.2f",tanb);
	tanb_v[counter_tb] = tanb;
	TString Tanb(tanb_str);
	TString fileName = folder + "/higgsCombine.mssm_tanb"+Tanb+".AsymptoticLimits.mH"+mass+".root";
	//	std::cout << fileName << std::endl;

	TFile * file = new TFile(fileName);
	TTree * tree = (TTree*)file->Get("limit");

	tree->SetBranchAddress("limit",&LIMIT);
	tree->SetBranchAddress("mh",&MH);

	tree->GetEntry(0);
	minus2_v[counter_tb] = float(LIMIT);
    
	tree->GetEntry(1);
	minus1_v[counter_tb] = float(LIMIT);

	tree->GetEntry(2);
	median_v[counter_tb] = float(LIMIT);

	tree->GetEntry(3);
	plus1_v[counter_tb] = float(LIMIT);

	tree->GetEntry(4);
	plus2_v[counter_tb] = float(LIMIT);

	tree->GetEntry(5);
	obs_v[counter_tb] = float(LIMIT);

	counter_tb++;
	tanb += dtanb;

    }

    minus2R[counter] = interpolate(counter_tb,tanb_v,minus2_v);
    minus1R[counter] = interpolate(counter_tb,tanb_v,minus1_v);
    medianR[counter] = interpolate(counter_tb,tanb_v,median_v);
    plus1R[counter] = interpolate(counter_tb,tanb_v,plus1_v);
    plus2R[counter] = interpolate(counter_tb,tanb_v,plus2_v);

    mA[counter] = MH;
    obsR[counter] = interpolate(counter_tb,tanb_v,obs_v);

    if (blindData)
      obsR[counter] = medianR[counter];

    counter++; 
      
  }


  std::cout << " mA    -2s    -1s    exp    +1s    +2s   obs " << std::endl; 
  //           " 225   2.37   3.21   4.57   6.61   9.21  6.50
  //           "100  24.1  28.2  33.8  40.8  48.2  23.0


  for (int i=0; i<counter; ++i) {

    obs[i]    = obsR[i];
    minus2[i] = minus2R[i];
    minus1[i] = minus1R[i];
    median[i] = medianR[i];
    plus1[i]  = plus1R[i];
    plus2[i]  = plus2R[i];

    char strOut[200];
    if (blindData) sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f",
			   int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i]);
    else sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f %5.2f",
		 int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i],obs[i]);
    std::cout << strOut << std::endl;

  }
  
  float zeros[nPoints];
  float upper[nPoints];
  float lower[nPoints];
  float central[nPoints];
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

  TGraph * obsG = new TGraph(nPointsX, mA, obs);
  obsG->SetLineWidth(3);
  obsG->SetLineColor(1);
  obsG->SetLineWidth(2);
  obsG->SetMarkerColor(1);
  obsG->SetMarkerStyle(20);
  obsG->SetMarkerSize(1.4);

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
  innerBand->SetFillColor(TColor::GetColor("#85D1FBff"));
  innerBand->SetLineColor(TColor::GetColor("#85D1FBff"));

  TGraphAsymmErrors * outerBand = new TGraphAsymmErrors(nPointsX, mA, median, zeros, zeros, minus2, plus2);
  outerBand->SetFillColor(kYellow);
  outerBand->SetLineColor(kYellow);
  outerBand->SetFillColor(TColor::GetColor("#FFDF7Fff"));
  outerBand->SetLineColor(TColor::GetColor("#FFDF7Fff"));

  TH2F * frame = new TH2F("frame","",2,XMin,XMax,2,YMin,YMax);
  frame->GetXaxis()->SetTitle("#it{m}_{A} (GeV)");
  frame->GetYaxis()->SetTitle("tan#beta");
  frame->GetXaxis()->SetNdivisions(505);
  frame->GetYaxis()->SetNdivisions(206);
  frame->GetYaxis()->SetMoreLogLabels();
  frame->GetYaxis()->SetNoExponent();
  frame->GetYaxis()->SetTitleOffset(1.25);  
  frame->GetYaxis()->SetTitleSize(0.048);  
  

  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);

  frame->Draw();

  outerBand->Draw("3same");
  innerBand->Draw("3same");
  expG->Draw("lsame");
  if (!blindData)
    obsG->Draw("lpsame");

  float xLeg = 0.18;
  float yLeg = 0.83;
  float xLegend = 0.57;
  float yLegend = 0.41;
  float sizeLeg = 0.27;

  TLegend * leg = new TLegend(0.20,0.2,0.53,0.50);
  leg->SetFillColor(0);
  leg->SetTextSize(0.037);
  leg->SetBorderSize(1);
  leg->SetHeader(Title);
  if (!blindData) 
    leg->AddEntry(obsG,"Observed","lp");
  leg->AddEntry(expG,"Expected","l");
  leg->AddEntry(innerBand,"68% expected","f");
  leg->AddEntry(outerBand,"95% expected","f");
  leg->Draw();

  extraText = "Preliminary";
  writeExtraText = true;
  CMS_lumi(canv,4,0,0.04); 
  canv->SetLogx(logx);
  canv->SetLogy(logy);
  canv->RedrawAxis();
  canv->SetGridy(true);
  canv->SetGridx(true);

  leg->Draw();
  canv->Update();

  if (blindData)
    canv->Print("figures/Limits_"+model+"_exp.png");
  else 
    canv->Print("figures/Limits_"+model+"_obs.png");

}
