#include "HttStylesNew.cc"
#include "CMS_lumi.C"

// x1 = a*y1 + b
// x2 = a*y2 + b
// a = (x1-x2)/(y1-y2)
// b = x1 - a*y1
double linear_int(double x1, double x2, double y1, double y2) {
  double a = (x1-x2)/(y1-y2);
  double b = x1 - a*y1;
  return b;
}

int Find_2D(int nPoints, // sqrt(number_of_points) 
	    double x1, // lower boundary of r_qqH
	    double x2,  // upper boundary of r_qqH
	    double y1, // lower boundary of r_ggH
	    double y2, // upper boundar of r_ggH
	    double correct, // smooth out curve
	    TTree * limit, // tree
	    double dnll, // 1sigma = 1, 2ssigma = 4 
	    double * xbest,
	    double * ybest,
	    double * x,
	    double * ymin,
	    double * ymax
	    ) { 


  double deltaY = (y2-y1)/double(nPoints);
  double deltaX = (x2-x1)/double(nPoints);
  
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

  if (correct>0.0) {
    for (int iGraph=0; iGraph<nGraph; ++iGraph) {
      ymax[iGraph] -= correct*deltaY;
      ymin[iGraph] -= correct*deltaY;
      if (ymin[iGraph]<0.0) 
	ymin[iGraph]=0;
      if (ymax[iGraph]<0.0) 
	ymax[iGraph]=0;
    }
    //    nGraph -= 1;
  }
  delete hist;
  delete update;

  return nGraph;

}

// ++++++++++++++++++++++
// +++ Main subroutine
// ++++++++++++++++++++++

void Plot2Dscan(TString mass = "1000",
		bool BR_AZh = true,
		bool pb = true,
		bool unblind = true) {

  SetStyle();
  gROOT->SetBatch(true);
  
  map<TString, double> xmax_mass = {
    {"225",1.2},
    {"250",1.3},
    {"275",0.9},
    {"300",0.8},
    {"350",0.6},
    {"400",0.5},
    {"500",0.25},
    {"600",0.15},
    {"700",0.12},
    {"800",0.10},
    {"1000",0.08},
  };
  
  map<TString, double> ymax_mass = {
    {"225",0.9},
    {"250",1.0},
    {"275",0.9},
    {"300",0.7},
    {"350",0.5},
    {"400",0.5},
    {"500",0.25},
    {"600",0.15},
    {"700",0.12},
    {"800",0.10},
    {"1000",0.08},
  };
  
  map<TString, double> corrections = {
    {"225",-1.},
    {"250",0.1},
    {"275",1.2},
    {"300",-1.},
    {"350",0.2},
    {"400",0.1},
    {"500",-1.},
    {"600",-1.},
    {"700",-1.},
    {"800",1.5},
    {"1000",0.3}
  };

  double correct = corrections[mass];
  double xmax_frame = xmax_mass[mass];
  double ymax_frame = ymax_mass[mass];
  
  double scaleBR = 1.0;
  if (BR_AZh) scaleBR = 1.0/(0.1*0.062);
  if (pb) scaleBR *= 1e-3;
  TString unit = "fb";
  if (pb) unit = "pb";

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
  double dx = xmax/double(nPoints);
  double dy = ymax/double(nPoints);


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

  int nGraph_1sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,correct,treeE,
			      dnll_1sigma,xbest,ybest,x_1sigma,ylow_1sigma,yhigh_1sigma);
  int nGraph_2sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,correct,treeE,
			      dnll_2sigma,xbest,ybest,x_2sigma,ylow_2sigma,yhigh_2sigma);

  int nGraphE_1sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,correct,tree,
			       dnll_1sigma,xbestE,ybestE,xE_1sigma,ylowE_1sigma,yhighE_1sigma);
  int nGraphE_2sigma = Find_2D(nPoints,xmin,xmax,ymin,ymax,correct,tree,
			       dnll_2sigma,xbestE,ybestE,xE_2sigma,ylowE_2sigma,yhighE_2sigma);

  for (int i=0; i<nGraph_1sigma; ++i) {
    double ycenter = 0.5*(yhigh_1sigma[i]+ylow_1sigma[i]);
    double yup = yhigh_1sigma[i] - ycenter;
    double ydown = ycenter - ylow_1sigma[i];
    ycentre_1sigma[i] = scaleBR*ycenter;
    yhigh_1sigma[i] = scaleBR*yup;
    ylow_1sigma[i] = scaleBR*ydown;
    x_1sigma[i] *= scaleBR;
  }

  for (int i=0; i<nGraph_2sigma; ++i) {
    double ycenter = 0.5*(yhigh_2sigma[i]+ylow_2sigma[i]);
    double yup = yhigh_2sigma[i] - ycenter;
    double ydown = ycenter - ylow_2sigma[i];
    ycentre_2sigma[i] = scaleBR*ycenter;
    yhigh_2sigma[i] = scaleBR*yup;
    ylow_2sigma[i] = scaleBR*ydown;
    x_2sigma[i] *= scaleBR;
  }
  
  TGraphAsymmErrors * contour_1sigma = new TGraphAsymmErrors(nGraph_1sigma, 
							     x_1sigma, 
							     ycentre_1sigma, 
							     xe, 
							     xe, 
							     ylow_1sigma, 
							     yhigh_1sigma);
  contour_1sigma->SetFillColor(TColor::GetColor("#85D1FBff"));
  contour_1sigma->SetLineColor(TColor::GetColor("#85D1FBff"));


  TGraphAsymmErrors * contour_2sigma = new TGraphAsymmErrors(nGraph_2sigma, 
							     x_2sigma, 
							     ycentre_2sigma, 
							     xe, 
							     xe, 
							     ylow_2sigma, 
							     yhigh_2sigma);
  contour_2sigma->SetFillColor(TColor::GetColor("#FFDF7Fff"));
  contour_2sigma->SetLineColor(TColor::GetColor("#FFDF7Fff"));

  int NP = nGraphE_1sigma-1;
  for (int ip=NP; ip>0; --ip) {
    if (ylowE_1sigma[ip]<dy&&ylowE_1sigma[ip]>0) {
      xE_1sigma[nGraphE_1sigma]=linear_int(xE_1sigma[ip-1],
					   xE_1sigma[ip],
					   yhighE_1sigma[ip-1],
					   yhighE_1sigma[ip]);
      yhighE_1sigma[nGraphE_1sigma]=0.;
      nGraphE_1sigma++;
      break;
    }
    else {
      xE_1sigma[nGraphE_1sigma]=xE_1sigma[ip];		
      yhighE_1sigma[nGraphE_1sigma]=ylowE_1sigma[ip];
      nGraphE_1sigma++;
    }
  }
  
  NP = nGraphE_2sigma-1;
  for (int ip=NP; ip>0; --ip) {
    if (ylowE_2sigma[ip]<dy&&ylowE_2sigma[ip]>0) {
      xE_2sigma[nGraphE_2sigma]=linear_int(xE_2sigma[ip-1],
					   xE_2sigma[ip],
					   yhighE_2sigma[ip-1],
					   yhighE_2sigma[ip]);
      yhighE_2sigma[nGraphE_2sigma]=0.;
      nGraphE_2sigma++;
      break;
    }
    else {
      xE_2sigma[nGraphE_2sigma]=xE_2sigma[ip];		
      yhighE_2sigma[nGraphE_2sigma]=ylowE_2sigma[ip];
      nGraphE_2sigma++;
      
    }
  }
  
  for (int iPoint=0; iPoint<nGraphE_1sigma; ++iPoint) {
    xE_1sigma[iPoint] *= scaleBR;
    yhighE_1sigma[iPoint] *= scaleBR;
  }

  for (int iPoint=0; iPoint<nGraphE_2sigma; ++iPoint) {
    xE_2sigma[iPoint] *= scaleBR;
    yhighE_2sigma[iPoint] *= scaleBR;
  }

  TGraph * graph_1sigma = new TGraph(nGraphE_1sigma,xE_1sigma,yhighE_1sigma);
  graph_1sigma->SetLineColor(kBlack);
  graph_1sigma->SetLineStyle(1);
  graph_1sigma->SetLineWidth(3);

  TGraph * graph_2sigma = new TGraph(nGraphE_2sigma,xE_2sigma,yhighE_2sigma);
  graph_2sigma->SetLineColor(kBlack);
  graph_2sigma->SetLineStyle(2);
  graph_2sigma->SetLineWidth(3);

  //Best fit 
  xbestE[0] *= scaleBR;
  ybestE[0] *= scaleBR;
  TGraph * graphBest = new TGraph(1,xbestE,ybestE);
  graphBest->SetMarkerStyle(34);
  graphBest->SetMarkerSize(3.);
  graphBest->SetMarkerColor(kBlack);

  TH2D * frame = new TH2D("frame","",2,xmin_frame,xmax_frame,2,ymin_frame,ymax_frame);
  if (BR_AZh) {
    frame->GetXaxis()->SetTitle("#sigma(gg#rightarrowA)#timesB(A#rightarrowZh) ["+unit+"]");
    frame->GetYaxis()->SetTitle("#sigma(bbA)#timesB(A#rightarrowZh) ["+unit+"]");
  }
  else {
    frame->GetXaxis()->SetTitle("#sigma(gg#rightarrowA)#timesB(A#rightarrowZh)#timesB(Z#rightarrowll)#timesB(h#rightarrow#tau#tau) ["+unit+"]");
    frame->GetYaxis()->SetTitle("#sigma(bbA)#timesB(A#rightarrowZh)#timesB(Z#rightarrowll)#timesB(h#rightarrow#tau#tau) ["+unit+"]");
  }

  frame->GetXaxis()->SetTitleOffset(1.3);
  frame->GetYaxis()->SetTitleOffset(1.7);

  frame->GetXaxis()->SetTitleSize(0.045);
  frame->GetYaxis()->SetTitleSize(0.045);

  frame->GetXaxis()->SetNdivisions(206);
  frame->GetYaxis()->SetNdivisions(206);

  frame->GetXaxis()->SetLabelOffset(0.02);
  frame->GetYaxis()->SetLabelOffset(0.02);

  frame->GetXaxis()->SetLabelSize(0.045);
  frame->GetYaxis()->SetLabelSize(0.045);

  TCanvas * canv = MakeCanvas("canv","",800,700);    
  frame->Draw();
  contour_2sigma->Draw("3same");
  contour_1sigma->Draw("3same");
  if (unblind) {
    graph_1sigma->Draw("lsame");
    graph_2sigma->Draw("lsame");
    graphBest->Draw("psame");
  }

  TLegend * leg = new TLegend(0.68,0.6,0.93,0.9);
  leg->SetFillColor(0);
  leg->SetBorderSize(1);
  leg->SetTextSize(0.033);
  leg->SetHeader("  #it{m}_{A} = "+mass+" GeV");
  leg->AddEntry(contour_1sigma,"  68% CL exp.","f");
  leg->AddEntry(contour_2sigma,"  95% CL exp.","f");
  if (unblind) {
    leg->AddEntry(graph_1sigma,"  68% CL obs.","l");
    leg->AddEntry(graph_2sigma,"  95% CL obs.","l");
    leg->AddEntry(graphBest,"  Best fit","p");
  }

  lumi_13TeV = "138 fb^{-1}";
  extraText = "Preliminary";
  writeExtraText = true;
  CMS_lumi(canv,4,0,0.03); 
  canv->SetGridx(true);
  canv->SetGridy(true);
  canv->RedrawAxis();
  leg->Draw();
  canv->Update();

  canv->Print("figures/"+folder+"_"+unit+".png");

}
