void ConvertLimits(double limit = 1.0,
		   bool reverse = false) {

  double scaleBR = 1e-3/(0.1*0.062);
  double limit_AZh_lltautau = limit;
  double limit_AZh = scaleBR * limit_AZh_lltautau;
  if (reverse) {
    scaleBR = 1000.*0.1*0.062;
    limit_AZh = limit;
    limit_AZh_lltautau = scaleBR * limit_AZh;
  }
  
  std::cout << "limit on BR(A->Zh->(ll)(tt) = " << limit_AZh_lltautau << std::endl;
  std::cout << "limit on BR(A->Zh)          = " << limit_AZh << std::endl;
  

}
