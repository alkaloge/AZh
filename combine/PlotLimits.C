#include "HttStylesNew.cc"
#include "CMS_lumi.C"

void PlotLimits(TString Era = "Run2", // year
		TString Sample = "Run2", // options : 2016, 2017, 2018, Run2, et, mt, tt
		TString Process = "bbA", // process
		TString folder = "limits", // input folder (output of macro RunLimits.py)
		TString postfix = "noFitAsimov",
		float YMax = 20, // upper boundary of Y axis
		float XMin = 225., // lower boundary of X axis
		float XMax = 2000., // upper boundary of X axis
		bool logx = false, // log scale of X axis
		bool blindData = true // blinding observed limit
		) {


  std::vector<TString> masses = {"225","250","275","300","325","350","375","400","450","500","600","700","800","900","1000","1200","1400","1600","1800","2000"};

  std::map<TString,TString> lumiLabel = {
    {"Run2","Run 2, 138 fb^{-1}"},
    {"2018","2018, 59.8 fb^{-1}"},
    {"2017","2017, 41.5 fb^{-1}"},
    {"2016","2016, 36.3 fb^{-1}"}
  };

  lumi_13TeV = lumiLabel[Era];


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

  double MH;
  double LIMIT;

  int counter = 0;

  for (auto mass : masses) {

    TString fileName = folder + "/higgsCombine.azh_"+Sample+"_"+Process+".AsymptoticLimits.mH"+mass+".root";
    std::cout << fileName << std::endl;

    TFile * file = new TFile(fileName);

    TTree * tree = (TTree*)file->Get("limit");

    //    std::cout << "file : " << file << std::endl;
    //    std::cout << "tree : " << tree << std::endl;

    tree->SetBranchAddress("limit",&LIMIT);
    tree->SetBranchAddress("mh",&MH);

    tree->GetEntry(0);
    mA[counter] = float(MH);
    minus2R[counter] = float(LIMIT);

    //    std::cout << mA[counter] << std::endl;
    
    tree->GetEntry(1);
    minus1R[counter] = float(LIMIT);

    tree->GetEntry(2);
    medianR[counter] = float(LIMIT);

    tree->GetEntry(3);
    plus1R[counter] = float(LIMIT);

    tree->GetEntry(4);
    plus2R[counter] = float(LIMIT);

    tree->GetEntry(5);
    obsR[counter] = float(LIMIT);
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

  TH2F * frame = new TH2F("frame","",2,XMin,XMax,2,0,YMax);
  frame->GetXaxis()->SetTitle("m_{A} (GeV)");
  frame->GetYaxis()->SetTitle("#sigma("+Process+")#timesB(A#rightarrowZh) [fb]");
  frame->GetXaxis()->SetNdivisions(505);
  frame->GetYaxis()->SetNdivisions(206);
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

  TLegend * leg = new TLegend(0.40,0.60,0.70,0.80);
  leg->SetFillColor(0);
  leg->SetTextSize(0.035);
  leg->SetBorderSize(0);
  if (!blindData) 
    leg->AddEntry(obsG,"Observed","lp");
  leg->AddEntry(expG,"Expected","l");
  leg->AddEntry(innerBand,"#pm1#sigma Expected","f");
  leg->AddEntry(outerBand,"#pm2#sigma Expected","f");
  leg->Draw();

  extraText = "Preliminary";
  writeExtraText = true;
  CMS_lumi(canv,4,33); 
  canv->SetLogx(logx);
  canv->RedrawAxis();

  leg->Draw();
  canv->Update();

  if (blindData)
    canv->Print("figures/Limits_"+Process+"_"+Sample+"_"+postfix+"_exp.png");
  else 
    canv->Print("figures/Limits_"+Process+"_"+Sample+"_"+postfix+"_obs.png");

}
