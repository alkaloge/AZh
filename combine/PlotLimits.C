#include "HttStylesNew.cc"
#include "CMS_lumi.C"

void PlotLimits(TString Era = "Run2",    // dataset : 2016, 2017, 2018, Run2
		TString Sample = "Run2", // options : 2016, 2017, 2018, Run2, et, mt, tt, btag, 0btag
		TString Process = "bbA", // process : ggA, bbA
		TString folder = "limits_obs", // input folder (output of macro RunLimits.py)
		TString postfix = "pas",     // postfix in the name of output png file
		float YMin = 0.0,   // lower boundary of Y axis 
		float YMax = 1.2,   // upper boundary of Y axis
		float XMin = 225.,  // lower boundary of X axis
		float XMax = 1000., // upper boundary of X axis
		bool logy = false, // log scale of Y axis
		bool logx = true,  // log scale of X axis
		float xLeg = 0.65, // x coordinate of the legend box
		float yLeg = 0.6, // y coordinate of the legend box
		bool BR_AZh = true, // produce results in terms of sigma x BR(A->Zh)
		bool pb = true,     // limits in picobarn
		bool blindData = false // blinding observed limit?
		) {


  double scaleBR = 1.0;
  if (BR_AZh) scaleBR = 1.0/(0.1*0.062);
  if (pb) scaleBR *= 1e-3; 
  TString unit = "fb";
  if (pb) unit = "pb";

  std::vector<TString> masses = {"225","250","275","300","325","350","375","400","450","500","600","700","800","900","1000","1200","1400","1600","1800","2000"};

  std::map<TString,TString> lumiLabel = {
    {"Run2","138 fb^{-1}"},
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
    minus2R[counter] = float(LIMIT)*scaleBR;
    
    tree->GetEntry(1);
    minus1R[counter] = float(LIMIT)*scaleBR;

    tree->GetEntry(2);
    medianR[counter] = float(LIMIT)*scaleBR;

    tree->GetEntry(3);
    plus1R[counter] = float(LIMIT)*scaleBR;

    tree->GetEntry(4);
    plus2R[counter] = float(LIMIT)*scaleBR;

    tree->GetEntry(5);
    obsR[counter] = float(LIMIT)*scaleBR;
    if (blindData)
      obsR[counter] = medianR[counter];

    counter++; 
      
  }


  std::cout << " mA    -2s    -1s    exp    +1s    +2s     obs " << std::endl; 
  //           "225   2.37   3.21   4.57   6.61   9.21  6.50


  for (int i=0; i<counter; ++i) {

    obs[i]    = obsR[i];
    minus2[i] = minus2R[i];
    minus1[i] = minus1R[i];
    median[i] = medianR[i];
    plus1[i]  = plus1R[i];
    plus2[i]  = plus2R[i];

    char strOut[200];
    if (BR_AZh) {
      if (pb) {
	if (blindData) sprintf(strOut,"%4i  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f",
			       int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i]);
	else sprintf(strOut,"%4i  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f   %5.3f",
		     int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i],obs[i]);	
      }
      else {
	if (blindData) sprintf(strOut,"%4i  %5.0f  %5.0f  %5.0f  %5.0f  %5.0f",
			       int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i]);
	else sprintf(strOut,"%4i  %5.0f  %5.0f  %5.0f  %5.0f  %5.0f   %5.0f",
		     int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i],obs[i]);
      }
    }
    else {
      if (blindData) sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f",
			     int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i]);
      else sprintf(strOut,"%4i  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f %5.2f",
		   int(mA[i]),minus2[i],minus1[i],median[i],plus1[i],plus2[i],obs[i]);
    }
    std::cout << strOut << std::endl;

  }

  double zeros[nPoints];
  double upper[nPoints];
  double lower[nPoints];
  double central[nPoints];
  for (int i=0; i<counter; ++i) {
    zeros[i] = 0;
    central[i] = 15.0*scaleBR; 
    minus2[i] = median[i] - minus2[i];
    minus1[i] = median[i] - minus1[i];
    plus1[i]  = plus1[i]  - median[i];
    plus2[i]  = plus2[i]  - median[i];
    upper[i] = 15.0*scaleBR - central[i];
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
  frame->GetXaxis()->SetTitle("m_{A} (GeV)");
  std::map<TString, TString> process = {
    {"bbA","bbA"},
    {"ggA","gg#rightarrowA"}
  };
  if (BR_AZh) {
    frame->GetYaxis()->SetTitle("#sigma("+process[Process]+")#timesB(A#rightarrowZh) ["+unit+"]");
  }
  else {
    frame->GetYaxis()->SetTitle("#sigma("+process[Process]+")#timesB(A#rightarrowZh)#timesB(Z#rightarrowll)#timesB(h#rightarrow#tau#tau) ["+unit+"]");
  }
  frame->GetXaxis()->SetNdivisions(510);
  frame->GetYaxis()->SetNdivisions(210);
  frame->GetXaxis()->SetMoreLogLabels(2);
  frame->GetXaxis()->SetNoExponent();
  frame->GetYaxis()->SetTitleOffset(1.3);  
  frame->GetYaxis()->SetTitleSize(0.05);  
  

  TString Header = process[Process];

  TCanvas *canv = MakeCanvas("canv", "histograms", 700, 600);

  frame->Draw();

  outerBand->Draw("3same");
  innerBand->Draw("3same");
  expG->Draw("lsame");
  if (!blindData)
    obsG->Draw("lpsame");

  TLegend * leg = new TLegend(xLeg,yLeg,xLeg+0.27,yLeg+0.3);
  leg->SetFillColor(0);
  leg->SetTextSize(0.035);
  leg->SetBorderSize(1);
  leg->SetHeader(Header);
  if (!blindData) 
    leg->AddEntry(obsG,"Observed","lp");
  leg->AddEntry(expG,"Expected","l");
  leg->AddEntry(innerBand,"68% expected","f");
  leg->AddEntry(outerBand,"95% expected","f");
  leg->Draw();

  extraText = "Preliminary";
  writeExtraText = true;
  CMS_lumi(canv,4,0,0.02); 
  canv->SetLogx(logx);
  canv->SetLogy(logy);
  canv->SetGridx(true);
  canv->SetGridy(true);
  canv->RedrawAxis();

  leg->Draw();
  canv->Update();

  if (blindData)
    canv->Print("figures/Limits_"+Process+"_"+Sample+"_"+postfix+"_exp.png");
  else 
    canv->Print("figures/Limits_"+Process+"_"+Sample+"_"+postfix+"_obs.png");

}
