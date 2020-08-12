# Author : S Middleton
# Date : 2020
# Purpose : Functions associated with the DIO

import sys
from ROOT import TF1, TCanvas
class DIO :

    def __init__(self):
        self.process = "DIO"

    """
    Function to calculate and integrate the DIO spectrum. The following approximation
    is from Czarnecki etal, 'Muon decay in orbit:spectrum of high-energy electrons',
    for E>85 MeV
    """
    def DIOcz(self, x, par):
        ee = x[0];
        norm = par[0];
        mal = 25133
        mmu = 105.654
        emu = 105.194
        emue = 104.973
        me = 0.511
        a5 = 8.6434e-17
        a6 = 1.16874e-17
        a7 = -1.87828e-19
        a8 = 9.16327e-20
        delta = emu - ee - ee*ee/(2*mal)
        if(delta > 0.0):
            return norm*(a5*pow(delta,5) + a6*pow(delta,6) + a7*pow(delta,7) + a8*pow(delta,8))
        else:
            return 0.0

    def DIOWeight(self, x):
        ee = x
        mal = 25133
        emu = 105.194

        a5 = 8.6434e-17
        a6 = 1.16874e-17
        a7 = -1.87828e-19
        a8 = 9.16327e-20
        delta = emu - ee - ee*ee/(2*mal)
        if(delta > 0.0):
            return (a5*pow(delta,5) + a6*pow(delta,6) + a7*pow(delta,7) + a8*pow(delta,8))
        else:
            return 0.0

    def GetDIOIntegral(self, mom_low, mom_high):
        c1 = TCanvas()
        _diocz_f = TF1("_diocz_f",self.DIOcz, 90,110.,1)
        _diocz_f.SetParameter(0,1.0)
        _diocz_f.Draw()
        c1.SaveAs("DIO.root")
        return _diocz_f.Integral(mom_low,mom_high)
