#!/usr/bin/env python

import ROOT

a = ROOT.Math.chisquared_quantile_c(1 - 0.95, 2)
b = ROOT.Math.chisquared_quantile_c(1 - 0.68, 2)
print(a,b)
