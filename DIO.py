# Author : S Middleton
# Date : 2020
# Purpose : Functions associated with the DIO

import sys

class DIO :

    def __init__(self):
        self.process = "DIO"

    """
    Function to calculate and integrate the DIO spectrum. The following approximation
    is from Czarnecki etal, 'Muon decay in orbit:spectrum of high-energy electrons',
    for E>85 MeV
    """
    def DIOCcz(self, x, par):
        double ee = x[0];
        double norm = par[0];
        mal = 25133
        mmu = 105.654
        emu = 105.194
        emue = 104.973
        double me = 0.511
        a5 = 8.6434e-17
        a6 = 1.16874e-17
        a7 = -1.87828e-19
        a8 = 9.16327e-20
        delta = emu - ee - ee*ee/(2*mal);
        if(delta > 0.0):
            return norm*(a5*pow(delta,5) + a6*pow(delta,6) + a7*pow(delta,7) + a8*pow(delta,8));
        else:
            return 0.0
