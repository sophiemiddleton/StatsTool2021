#TODO:

class YieldFunctions:

        def __init__(self):
            self.signal_start = 103.75
            self.signal_end = 105.45
            self.livegate = 700.
            self.POT = 3.6e20
            self.capturesperStop = 0.609
            self.muonstopsperPOT = 0.00159
            self.Mu2eXBR = 5e-5

        def SignalRegionStart(self):
            return self.signal_start

        def SignalRegionEnd(self):
            return self.signal_end

        def GetPOT(self):
            return self.POT

        def CapturesPerStop(self):
            return self.capturesperStop

        def MuonStopsPerPOT(self):
            return self.muonstopsperPOT

        def Mu2eXBF(self):
            return self.Mu2eXBR

        def GetIntegral(self, histo, mom_low, mom_high):
            # Translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth()) + 1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth()) + 1
            return histo.Integral(bin_low,bin_high)

        def GetN(self, histo, mom_low, mom_high):
            Nrec = self.GetIntegral(histo, mom_low, mom_high)
            return Nrec

        def GetNError(self, histo, mom_low,  mom_high):
            Nrec_error = 0
            # compute error from sum of weigths in the bins
            # translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth())+1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth())+1
            temp_error_sum = 0
            for i in range(bin_low, bin_high):
                temp_error_sum += pow(histo.GetBinError(i), 2)
            Nrec_error = math.sqrt(temp_error_sum)
            return Nrec_error

        def GetRecoEff(self, Nrec, Ngen):
            efficiency = Nrec / Ngen
            return efficiency

        def GetRecoEffError(self, Nrec, Ngen):
            """
            use Glen Cowan derivation of efficiency error based on a binomial distribution
            http://www.pp.rhul.ac.uk/~cowan/stat/notes/efferr.pdf
            """
            efficiency_error = math.sqrt(Nrec * (1. - Nrec/Ngen)) / Ngen
            return efficiency_error

        def GetExpectedYield(self, mom_low, mom_high, eff):
            N_expected = self.GetPOT() * self.MuonStopsPerPOT() * self.Mu2eXBF() *  eff
            N_expected_error = 0
            return N_expected, N_expected_error
