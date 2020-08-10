# Author : S Middleton
# Date : 2020
# Purpose : class to store histograms

import sys
import ROOT
from ROOT import TMath, TF1, TH1F

class Histograms :
    def __init__(self, nBins, momentum_lower_limit, momentum_upper_limit):
        _diocz_f = ROOT.TF1("_diocz_f",DIOCZ,momentum_lower_limit,momentum_upper_limit,1);
    	_diocz_f.SetLineColor(kGreen);
    	_diocz_f.SetParameter(0,1.0);

    	self.histo_CE_reconstructed = ROOT.TH1F("histo_CE_reconstructed","histo_CE_reconstructed",nBins,momentum_lower_limit,momentum_upper_limit)
    	self.histo_CE_generated = ROOT.TH1F("histo_CE_generated","histo_CE_generated",nBins,momentum_lower_limit,momentum_upper_limit)
    	self.histo_DIO_reconstructed_flat = ROOT.TH1F("histo_DIO_reconstructed_flat","histo_DIO_reconstructed_flat",nBins,momentum_lower_limit,momentum_upper_limit)
    	self.self.histo_DIO_generated_flat = ROOT.TH1F("histo_DIO_generated_flat","histo_DIO_generated_flat",nBins,momentum_lower_limit,momentum_upper_limit)
    	self.histo_DIO_reconstructed_reweighted = ROOT.TH1F("histo_DIO_reconstructed_reweighted","histo_DIO_reconstructed_reweighted",nBins,momentum_lower_limit,momentum_upper_limit)
    	self.histo_DIO_generated_reweighted = ROOT.TH1F("histo_DIO_generated_reweighted","histo_DIO_generated_reweighted",nBins,momentum_lower_limit,momentum_upper_limit)

    	self.histo_CE_reconstructed.Sumw2()
    	self.histo_CE_generated.Sumw2()
    	self.histo_DIO_reconstructed_flat.Sumw2()
    	self.histo_DIO_generated_flat.Sumw2()
    	self.histo_DIO_reconstructed_reweighted.Sumw2()
    	self.histo_DIO_generated_reweighted->Sumw2()
