void ConvertLimits(double limit) {

  double scaleBR = 1e-3/(0.1*0.062);
  double limit_AZh = scaleBR * limit;

  std::cout << "limit on BR(A->Zh->(ll)(tt) = " << limit << std::endl;
  std::cout << "limit on BR(A->Zh)          = " << limit_AZh << std::endl;
  

}
