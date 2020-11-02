# Author : S Middleton
# Date : 2020
# Purpose : Functions associated with the Mu2eX

import sys
from ROOT import TF1
import scipy.integrate as integrate

class Mu2eX :

    def __init__(self):
        self.process = "Mu2eX"
    """
    Mu(-) --> e(-) + X where X is a light boson. Spectrum based on Spectrum based on arXiv: 1110.2874
    """
    def Mu2eXcz(self, x):
        ee = x;
        norm = 1; #par[0];
        mal = 25133
        mmu = 105.6584
        emu = 105.194
        emue = 104.973
        me = 0.511
        BR = 5e-5
        Gamma = 2.99561e-16
        a0 = 3.289e-10
        a1 = 3.137e-7
        a2 = 1.027e-4
        a3 = 1.438e-3
        a4 = 2.419e-3
        a5 = 1.215e-1
        delta = ((emu - x - pow(x,2)/(2*mal))/mmu)
        if(delta > 0.0):
            return BR*(1/mmu)*(a0*pow(delta,1) + a1*pow(delta,2) + a2*pow(delta,3) + a3*pow(delta,4) + a4*pow(delta,5) + a5*pow(delta,6));
        else:
            return 0.0

    def Mu2eXWeight(self, x):
        ee = x;
        norm = 1; #par[0];
        mal = 25133
        mmu = 105.6584
        emu = 105.194
        emue = 104.973
        me = 0.511
        BR = 5e-5;
        Gamma = 2.99561e-16;
        a0 = 3.289e-10;
        a1 = 3.137e-7;
        a2 = 1.027e-4;
        a3 = 1.438e-3;
        a4 = 2.419e-3;
        a5 = 1.215e-1;
        delta = ((emu - x - pow(x,2)/(2*mal))/mmu)
        if(delta > 0.0):
            return BR*(1/mmu)*(a0*pow(delta,1) + a1*pow(delta,2) + a2*pow(delta,3) + a3*pow(delta,4) + a4*pow(delta,5) + a5*pow(delta,6));
        else:
            return 0.0

    def GetMu2eXIntegral(self, mom_low, mom_high):
        _Mu2eXcz_f = TF1("_Mu2eXcz_f",self.Mu2eXcz, 100,110.,1)
        #_Mu2eXcz_f.SetParameter(0,1.0)
        return _Mu2eXcz_f.Integral(mom_low,mom_high)

    def GetInt(self,mom_low, mom_high):
        f = lambda x:self.Mu2eXcz(x)
        intergral = integrate.quad(f, mom_low,mom_high)
        print("intergral",intergral)
        return intergral[0]

    def GetNgen(self):
        return self.Ngen
