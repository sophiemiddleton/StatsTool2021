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
from Histograms import Histograms
from Mu2eNegFunctions import *
from Results import Results
from ROOT import TCanvas


def main(options, args):
    print("Importing Data from: CE", options.CEReco, options.CEGen, "DIO",
options.DIOReco, options.DIOGen, "internal RPC", options.RPCintReco, options.RPCintGen,
"external RPC", options.RPCextReco, options.RPCextGen, options.Cosmics)
    UsePandas(400, 90., 110.)

def UsePandas(nbins, mom_low, mom_high,):
    recodata = ImportRecoData(options.CEReco, options.DIOReco, options.RPCextReco, options.RPCintReco)
    gendata = ImportGenData(options.CEGen, options.DIOGen, options.RPCextGen, options.RPCintGen)
    histos = Histograms(nbins, mom_low, mom_high,)
    showRPC = options.showRPC
    #Get Data:
    DIO_reco_mom = recodata.GetFeature( "DIO", "deent.mom")
    CE_reco_mom = recodata.GetFeature( "CE", "deent.mom")

    # Fill Reco Hists:
    histos.FillHistogram(histos.histo_CE_reconstructed , CE_reco_mom)
    histos.FillHistogram(histos.histo_DIO_reconstructed_flat , DIO_reco_mom)
    if(showRPC):
        RPCext_reco_mom = recodata.GetFeature( "RPCext", "deent.mom")
        RPCint_reco_mom = recodata.GetFeature( "RPCint", "deent.mom")
        histos.FillHistogram(histos.histo_extRPC_reconstructed , RPCext_reco_mom)
        histos.FillHistogram(histos.histo_intRPC_reconstructed , RPCint_reco_mom)

    histos.DoDIOWeights(histos.histo_DIO_reconstructed_reweighted , DIO_reco_mom)

    # Fill Gen:
    DIO_gen_mom = gendata.GetFeature("DIO", "TMom")
    CE_gen_mom = gendata.GetFeature("CE", "TMom")
    #DIO_gen_mom = recodata.GetMagFeature("DIO", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    #CE_gen_mom = recodata.GetMagFeature("CE", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    # Fill Gen Hists:
    histos.FillHistogram(histos.histo_CE_generated , CE_gen_mom)
    histos.FillHistogram(histos.histo_DIO_generated_flat , DIO_gen_mom)

    if(showRPC):
        RPCext_gen_mom = gendata.GetFeature("RPCext","TMome")
        RPCint_gen_mom = gendata.GetFeature("RPCint","TMome")
        histos.FillHistogram(histos.histo_intRPC_generated , RPCint_gen_mom)
        histos.FillHistogram(histos.histo_extRPC_generated , RPCext_gen_mom)

    histos.DoDIOWeights(histos.histo_DIO_generated_reweighted , DIO_gen_mom)

    # Build Functions:
    stats = StatsFunctions()
    yields = YieldFunctions(histos, nbins, mom_low, mom_high, options.RPCintReco, options.RPCextReco, options.target, showRPC)

    # Fill Results
    #yields.FillResults()

    yields.GetSingleResult(103,105)
    yields.WriteHistograms()
def UseROOT(bins, mom_low, mom_high,):
    #Pass the .root TH1F's to histograms directly
    histos = Histograms(nbins, mom_low, mom_high,)
    showRPC = options.showRPC

    # Fill Reco Hists:
    histos.FillGenHistogramROOT(options.CEReco, options.DIOReco, options.RPCextReco, options.RPCintReco)
    histos.FillRecoHistogramROOT(options.CEGen, options.DIOGen, options.RPCextGen, options.RPCintGen)
    histos.DoDIOWeights(histos.histo_DIO_reconstructed_reweighted , DIO_reco_mom)
    histos.DoDIOWeights(histos.histo_DIO_generated_reweighted , DIO_gen_mom)

    # Build Functions:
    stats = StatsFunctions()
    yields = YieldFunctions(histos, nbins, mom_low, mom_high, options.RPCintReco, options.RPCextReco, options.target, showRPC)

    # Fill Results
    #yields.FillResults()
    yields.GetSingleResult(103,105)

def plot1DHist(file_name, tree_name, branch_name, feature_name):
    """ Basic funciton to make a plot of a feature """
    #To make a plot: plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")
    file = uproot.open(file_name)
    electrons = file[tree_name][branch_name]

    df = electrons.pandas.df(flatten=False)

    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(df[feature_name],
                               bins=100,
                               range=(0,140),
                               label="electrons")

    ax.set_ylabel('N')
    ax.set_xlabel(str(feature_name))
    fig.savefig(str(feature_name)+'.png')

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CEReco', dest='CEReco', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-o','--DIOReco', dest='DIOReco', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-v','--showRPC', dest='showRPC', default = 'True',help='include RPC', metavar='rpc')
    parser.add_option('-p','--RPCextReco', dest='RPCextReco', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-t','--RPCintReco', dest='RPCintReco', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-g','--CEGen', dest='CEGen', default = 'CEGen.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-l','--DIOGen', dest='DIOGen', default = 'DIOGen.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-k','--RPCextGen', dest='RPCextGen', default = 'RPCGen.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-u','--RPCintGen', dest='RPCintGen', default = 'RPCGen.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-c','--Cosmics', dest='Cosmics', default = 'False',help='NTuple with Cosmics', metavar='Cosmicsdir')
    parser.add_option('-s','--target', dest='target', default = 'mu2e',help='target', metavar='stopsdir')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
