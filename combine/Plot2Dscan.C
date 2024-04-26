#include "HttStylesNew.cc"
#include "CMS_lumi.C"
int Find_2D(int nPoints, // sqrt(number_of_points) 
	    double x1, // lower boundary of r_qqH
	    double x2,  // upper boundary of r_qqH
	    double y1, // lower boundary of r_ggH
	    double y2, // upper boundar of r_ggH
	    TTree * limit, // tree
	    double dnll, // 1sigma = 1, 2ssigma = 4 
	    double * xbest,
	    double * ybest,
	    double * x,
	    double * ymin,
	    double * ymax
	    ) { 


  double deltaY = (y2-y1)/double(nPoints);

  TCanvas * dummy = new TCanvas("dummy","",600,500);
  TH2D * hist   = new TH2D("hist",  "",nPoints,x1,x2,nPoints,y1,y2);
  TH2D * update = new TH2D("update","",nPoints,x1,x2,nPoints,y1,y2);
  limit->Draw("r_bbA:r_ggA>>hist","TMath::Min(2*deltaNLL,1000.)","r_bbA>0.00001&&r_ggA>0.00001");
  delete dummy;

  for (int i=1; i<=nPoints; ++i) {
    for (int j=1; j<=nPoints; ++j) {
      double value = hist->GetBinContent(i,j);
      double x = hist->GetXaxis()->GetBinCenter(i);
      double y = hist->GetYaxis()->GetBinCenter(j);
      if (value<1e-7) {
	value = 0.5*(hist->GetBinContent(i-1,j)+
		     hist->GetBinContent(i+1,j));
      }
      //      printf("[%5.2f,%5.2f] : %5.2f\n",x,y,value);
      update->SetBinContent(i,j,value);
    }
  }

  unsigned int imin = 0;
  unsigned int imax = 0;

  //  std::cout << "nPoints" << nPoints << std::endl;

  int nGraph = 0;
  double dnllMax = 10;
  for (int i=1; i<=nPoints; ++i) {
    double xP = update->GetXaxis()->GetBinLowEdge(i);
    bool foundHigh = update->GetBinContent(i,nPoints)<dnll;
    bool foundLow = update->GetBinContent(i,1)<dnll;
    double yHigh = update->GetYaxis()->GetBinLowEdge(nPoints);
    double yLow = update->GetYaxis()->GetBinLowEdge(1);
    for (int j=2; j<=nPoints-1; ++j) {
      double y1 = update->GetYaxis()->GetBinLowEdge(j-1);
      double y2 = update->GetYaxis()->GetBinLowEdge(j);
      double n1 = update->GetBinContent(i,j-1);
      double n2 = update->GetBinContent(i,j);
      if (n1<dnllMax) {
	dnllMax = n1;
	xbest[0] = xP;
	ybest[0] = y1;
      }
      if (n2<dnllMax) {
	dnllMax = n2;
	xbest[0] = xP;
	ybest[0] = y2;
      }
      if (n1<dnll&&n2>dnll) {
	double y = y1 + (dnll-n1)*(y2-y1)/(n2-n1);
	yHigh = y;
	foundHigh = true;
      }
      if (n1>dnll&&n2<dnll) {
	double y = y1 + (dnll-n1)*(y2-y1)/(n2-n1);
	yLow = y;
	foundLow = true;
      }
    }
    if (foundHigh&&foundLow) {
      x[nGraph] = xP;
      ymin[nGraph] = yLow;
      ymax[nGraph] = yHigh;
      nGraph++;
    }
  }	  
  std::cout << std::endl;
  for (unsigned int i=0; i<nGraph; ++i) 
    printf("%6.3f : %6.3f - %6.3f \n",x[i],ymin[i],ymax[i]);
  std::cout << std::endl;

  std::cout << std::endl;
  printf("(x,y) = (%5.3f,%5.3f) DNLL = %5.3f\n",xbest[0],ybest[0],dnllMax);

  delete hist;
  delete update;

  return nGraph;

}

// ++++++++++++++++++++++
// +++ Main subroutine
// ++++++++++++++++++++++
void Plot2Dscan(TString mass = "250",
		double xmax_frame = 3,
		double ymax_frame = 3) {

  SetStyle();

  TString folder = "2Dscan_Run2_" + mass;

  //  gROOT->SetBatch(true);

  TFile * fileInfo = new TFile(folder+"/Info_2D.root");
  if (fileInfo==NULL || fileInfo->IsZombie()) {
    std::cout << "File " << folder << "/Info_2D.root does not exist or not properly closed" << std::endl; 
    return;
  }

  TTree * treeInfo = (TTree*)fileInfo->Get("info");
  int nPoints;
  double xmax;
  double ymax;
  treeInfo->SetBranchAddress("npoints",&nPoints);
  treeInfo->SetBranchAddress("ggA_max",&xmax);
  treeInfo->SetBranchAddress("bbA_max",&ymax);
  treeInfo->GetEntry(0);
  
  std::cout << "npoints = " << nPoints << std::endl;
  std::cout << "xmax = " << xmax << std::endl;
  std::cout << "ymax = " << ymax << std::endl;
  //  return;


  TFile * file = new TFile(folder+"/Scan_obs.root");
  TFile * fileE = new TFile(folder+"/Scan_exp.root");
  if (file==NULL || file->IsZombie()) {
    std::cout << "File " << folder << "/Scan_obs.root does not exist or not properly closed" << std::endl;
    return;
  }

  if (fileE==NULL || fileE->IsZombie()) {
    std::cout << "File " << folder << "/Scan_exp.root does not exist or not properly closed" << std::endl;
    return;
  }
 
  TTree * tree = (TTree*)file->Get("limit");
  TTree * treeE = (TTree*)fileE->Get("limit");

  double xmin =  0.0;
  double ymin = 0.0;
  double dnll_1sigma = 2.28;
  double dnll_2sigma = 5.99;

  double x_1sigma[200];
  double ylow_1sigma[200];
  double yhigh_1sigma[200];
  double ycentre_1sigma[200];

  double x_2sigma[200];
  double ylow_2sigma[200];
  double yhigh_2sigma[200];
  double ycentre_2sigma[200];
  
  double xE_1sigma[200];
  double ylowE_1sigma[200];
  double yhighE_1sigma[200];
  double ycentreE_1sigma[200];

  double xE_2sigma[200];
  double ylowE_2sigma[200];
  double yhighE_2sigma[200];
  double ycentreE_2sigma[200];
  
  double xbest[1];
  double ybest[1];
  double xbestE[1];
  double ybestE[1];
  
  double xe[200];

  double xmin_frame = 0;
  double ymin_frame = 0;


  for (unsigned int i=0; i<200; ++i)
    xe[i] = 0;

  int nGraph_1sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,treeE,
			      dnll_1sigma,xbest,ybest,x_1sigma,ylow_1sigma,yhigh_1sigma);
  int nGraph_2sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,treeE,
			      dnll_2sigma,xbest,ybest,x_2sigma,ylow_2sigma,yhigh_2sigma);

  int nGraphE_1sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,tree,
			       dnll_1sigma,xbestE,ybestE,xE_1sigma,ylowE_1sigma,yhighE_1sigma);
  int nGraphE_2sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,tree,
			       dnll_2sigma,xbestE,ybestE,xE_2sigma,ylowE_2sigma,yhighE_2sigma);

  for (int i=0; i<nGraph_1sigma; ++i) {
    double ycenter = 0.5*(yhigh_1sigma[i]+ylow_1sigma[i]);
    double yup = yhigh_1sigma[i] - ycenter;
    double ydown = ycenter - ylow_1sigma[i];
    ycentre_1sigma[i] = ycenter;
    yhigh_1sigma[i] = yup;
    ylow_1sigma[i] = ydown;
  }

  for (int i=0; i<nGraph_2sigma; ++i) {
    double ycenter = 0.5*(yhigh_2sigma[i]+ylow_2sigma[i]);
    double yup = yhigh_2sigma[i] - ycenter;
    double ydown = ycenter - ylow_2sigma[i];
    ycentre_2sigma[i] = ycenter;
    yhigh_2sigma[i] = yup;
    ylow_2sigma[i] = ydown;
  }
  
  TGraphAsymmErrors * contour_1sigma = new TGraphAsymmErrors(nGraph_1sigma, 
							     x_1sigma, 
							     ycentre_1sigma, 
							     xe, 
							     xe, 
							     ylow_1sigma, 
							     yhigh_1sigma);
  contour_1sigma->SetFillColor(kGreen);
  contour_1sigma->SetLineColor(kGreen);


  TGraphAsymmErrors * contour_2sigma = new TGraphAsymmErrors(nGraph_2sigma, 
							     x_2sigma, 
							     ycentre_2sigma, 
							     xe, 
							     xe, 
							     ylow_2sigma, 
							     yhigh_2sigma);
  contour_2sigma->SetFillColor(kYellow);
  contour_2sigma->SetLineColor(kYellow);

  double xx = xE_1sigma[nGraphE_1sigma-1];
  xE_1sigma[nGraphE_1sigma] = xx;
  yhighE_1sigma[nGraphE_1sigma] = 0.;
  nGraphE_1sigma++;
  
  xx = xE_2sigma[nGraphE_2sigma-1];
  xE_2sigma[nGraphE_2sigma] = xx;
  yhighE_2sigma[nGraphE_2sigma] = 0.;
  nGraphE_2sigma++;
  

  TGraph * graph_1sigma = new TGraph(nGraphE_1sigma,xE_1sigma,yhighE_1sigma);
  graph_1sigma->SetLineColor(kBlue);
  graph_1sigma->SetLineStyle(2);
  graph_1sigma->SetLineWidth(3);

  TGraph * graph_2sigma = new TGraph(nGraphE_2sigma,xE_2sigma,yhighE_2sigma);
  graph_2sigma->SetLineColor(kRed);
  graph_2sigma->SetLineStyle(2);
  graph_2sigma->SetLineWidth(3);

  //Best fit 
  TGraph * graphBest = new TGraph(1,xbestE,ybestE);
  graphBest->SetMarkerStyle(43);
  graphBest->SetMarkerSize(4.0);
  graphBest->SetMarkerColor(kBlack);

  TH2D * frame = new TH2D("frame","",2,xmin_frame,xmax_frame,2,ymin_frame,ymax_frame);
  frame->GetXaxis()->SetTitle("#sigma(ggA)#timesBR [fb]");
  frame->GetYaxis()->SetTitle("#sigma(bbA)#timesBR [fb]");
  frame->GetYaxis()->SetTitleOffset(1.2);
  frame->GetXaxis()->SetTitleSize(0.06);
  frame->GetYaxis()->SetTitleSize(0.06);
  frame->GetXaxis()->SetNdivisions(206);
  frame->GetYaxis()->SetNdivisions(206);
  
  TCanvas * canv = MakeCanvas("canv","",800,700);    
  frame->Draw();

  contour_2sigma->Draw("3same");
  contour_1sigma->Draw("3same");
  graph_1sigma->Draw("lsame");
  graph_2sigma->Draw("lsame");
  graphBest->Draw("psame");

  TLegend * leg = new TLegend(0.7,0.45,0.85,0.75);
  SetLegendStyle(leg);
  leg->SetTextSize(0.033);
  leg->SetHeader("m_{A} = "+mass+" GeV");
  leg->AddEntry(contour_1sigma,"exp 68%","f");
  leg->AddEntry(contour_2sigma,"exp 95%","f");
  leg->AddEntry(graph_1sigma,"obs 68%","l");
  leg->AddEntry(graph_2sigma,"obs 95%","l");
  leg->AddEntry(graphBest,"best fit","p");
  leg->Draw();

  lumi_13TeV = "138 fb^{-1}";
  extraText = "Preliminary";
  writeExtraText = true;
  CMS_lumi(canv,4,33); 
  canv->RedrawAxis();
  canv->Update();
  canv->Print("figures/"+folder+".png");

}
