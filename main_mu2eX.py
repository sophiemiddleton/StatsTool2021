#!/usr/bin/python
# Author: S Middleton
# Date: 2020
# Purpose: Import Data to StatsTool

import uproot
import sys
import argparse
import math
from optparse import OptionParser
import matplotlib.pyplot as plt
from ImportRecoData import ImportRecoData
from ImportGenData import ImportGenData
from Histograms import *
from Mu2eXFunctions import *
from Results import Results
from ROOT import TCanvas


def main(options, args):
    UsePandas(400, 100, 105)

def UsePandas(nbins, mom_low, mom_high,):
    recodata = ImportRecoData(options.Mu2eXReco, options.DIOReco)
    gendata = ImportGenData(options.Mu2eXGen, options.DIOGen)
    histos = HistogramsMu2eX(nbins, mom_low, mom_high,)

    #Get Data:
    DIO_reco_mom = recodata.GetFeature( "DIO", "deent.mom")
    signal_reco_mom = recodata.GetFeature( "signal", "deent.mom")

    # Fill Reco Hists:
    histos.FillHistogram(histos.histo_Mu2eX_reconstructed , signal_reco_mom)
    histos.FillHistogram(histos.histo_DIO_reconstructed_flat , DIO_reco_mom)

    histos.DoDIOWeights(histos.histo_DIO_reconstructed_reweighted , DIO_reco_mom)
    histos.DoMu2eXWeights(histos.histo_Mu2eX_reconstructed_reweighted , DIO_reco_mom)
    # Fill Gen:
    DIO_gen_mom = gendata.GetFeature("DIO", "TMom")
    signal_gen_mom = gendata.GetFeature("signal", "TMom")

    # Fill Gen Hists:
    histos.FillHistogram(histos.histo_Mu2eX_generated , signal_gen_mom)
    histos.FillHistogram(histos.histo_DIO_generated_flat , DIO_gen_mom)

    histos.DoDIOWeights(histos.histo_DIO_generated_reweighted , DIO_gen_mom)
    histos.DoMu2eXWeights(histos.histo_Mu2eX_generated_reweighted , DIO_gen_mom)
    # Build Functions:
    stats = StatsFunctions()
    yields = YieldFunctions(histos, nbins, mom_low, mom_high)

    # Fill Results
    yields.FillResults()

    #yields.GetSingleResult(104,105, True)
    yields.WriteHistograms()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--Mu2eXReco', dest='Mu2eXReco', default = 'Mu2eXData.root',help='NTuple with Mu2eX', metavar='Cedir')
    parser.add_option('-o','--DIOReco', dest='DIOReco', default = '../mu2eX/RecoDIO.root',help='NTuple with DIO', metavar='Diodir')

    parser.add_option('-g','--Mu2eXGen', dest='Mu2eXGen', default = 'Mu2eXGen.root',help='NTuple with Mu2eX', metavar='Cedir')
    parser.add_option('-l','--DIOGen', dest='DIOGen', default = 'DIOGen.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
