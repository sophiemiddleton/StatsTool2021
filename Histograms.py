# Author : S Middleton
# Date : 2020
# Purpose : class to store histograms

import sys
import ROOT
from DIO import DIO
from ROOT import TMath, TH1F

class Histograms :
    def __init__(self, nBins, momentum_lower_limit, momentum_upper_limit, target_mass_scalefactor=1):

        self.histo_CE_reconstructed = TH1F("Reconstructed CE","Reconstructed CE",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_CE_generated = TH1F("Generated CE","Generated CE",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_DIO_reconstructed_flat = TH1F("Reconstructed DIO_flat","Reconstructed DIO_flat",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_DIO_generated_flat = TH1F("Generated DIO_flat","Generated DIO_flat",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_DIO_reconstructed_reweighted = TH1F("Reconstructed DIO_reweighted","Reconstructed DIO_reweighted",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_DIO_generated_reweighted = TH1F("Generated DIO_reweighted","Generated DIO_reweighted",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_RPC_reconstructed = TH1F("Reconstructed RPC","Reconstructed RPC",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_RPC_generated = TH1F("Generated RPC","Generated RPC",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_Cosmics_reconstructed = TH1F("histo_Cosmics_reconstructed","histo_Cosmics_reconstructed",nBins,momentum_lower_limit,momentum_upper_limit)
        self.histo_Cosmics_generated = TH1F("histo_Cosmics_generated","histo_Cosmics_generated",nBins,momentum_lower_limit,momentum_upper_limit)

        self.histo_CE_reconstructed.Sumw2()
        self.histo_CE_generated.Sumw2()
        self.histo_DIO_reconstructed_flat.Sumw2()
        self.histo_DIO_generated_flat.Sumw2()
        self.histo_DIO_reconstructed_reweighted.Sumw2()
        self.histo_DIO_generated_reweighted.Sumw2()
        self.histo_RPC_reconstructed.Sumw2()
        self.histo_RPC_generated.Sumw2()

        self.histo_RPC_reconstructed.Scale(target_mass_scalefactor)

    def FillHistogram(self, histogram, data):
        for i, j in enumerate(data):
            histogram.Fill(j)
        return histogram

    def DoDIOWeights(self, histogram, data):
        dio = DIO()
        for i, j in enumerate(data):
            dio_weight =  dio.DIOWeight(j)
            histogram.Fill(j, dio_weight / 7.91001e-10 )
