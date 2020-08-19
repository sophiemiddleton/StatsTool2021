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

def plot1DHist(file_name, tree_name, branch_name, feature_name):
    """ Basic funciton to make a plot of a feature """
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
    fig.savefig('UpRootExamplePlot.png')

def main(options, args):
    print("Importing Data from: CE", options.CEReco, options.CEGen, "DIO",
options.DIOReco, options.DIOGen, "internal RPC", options.RPCintReco, options.RPCintGen,
"external RPC", options.RPCextReco, options.RPCextGen)

    recodata = ImportRecoData(options.CEReco, options.DIOReco, options.RPCextReco, options.RPCintReco)
    gendata = ImportGenData(options.CEGen, options.DIOGen, options.RPCextGen, options.RPCintGen)
    histos = Histograms(400, 90., 110.)
    showRPC = options.noRPC
    #Get Data:
    DIO_reco_mom = recodata.GetFeature( "DIO", "deent.mom")
    CE_reco_mom = recodata.GetFeature( "CE", "deent.mom")

    # Fill Reco Hists:
    histos.FillHistogram(histos.histo_CE_reconstructed , CE_reco_mom)
    histos.FillHistogram(histos.histo_DIO_reconstructed_flat , DIO_reco_mom)
    #if(showRPC == False):
    RPCext_reco_mom = recodata.GetFeature( "RPCext", "deent.mom")
    RPCint_reco_mom = recodata.GetFeature( "RPCint", "deent.mom")
    histos.FillHistogram(histos.histo_extRPC_reconstructed , RPCext_reco_mom)
    histos.FillHistogram(histos.histo_intRPC_reconstructed , RPCint_reco_mom)

    histos.DoDIOWeights(histos.histo_DIO_reconstructed_reweighted , DIO_reco_mom)

    # Fill Gen:
    DIO_gen_mom = gendata.GetFeature("DIO", "TreeMom")
    CE_gen_mom = gendata.GetFeature("CE", "TreeMom")

    # Fill Gen Hists:
    histos.FillHistogram(histos.histo_CE_generated , CE_gen_mom)
    histos.FillHistogram(histos.histo_DIO_generated_flat , DIO_gen_mom)

    #if(showRPC == False):
    RPCext_gen_mom = gendata.GetFeature("RPCext","TMome")
    RPCint_gen_mom = gendata.GetFeature("RPCint","TMome")
    histos.FillHistogram(histos.histo_intRPC_generated , RPCint_gen_mom)
    histos.FillHistogram(histos.histo_extRPC_generated , RPCext_gen_mom)


    histos.DoDIOWeights(histos.histo_DIO_generated_reweighted , DIO_gen_mom)

    # Build Functions:
    stats = StatsFunctions()
    yields = YieldFunctions(histos, options.RPCintReco, options.RPCextReco, options.noRPC)

    # Fill Results
    yields.GetSingleResult()
    #To make a plot: plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CEReco', dest='CEReco', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-o','--DIOReco', dest='DIOReco', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-v','--noRPC', dest='noRPC', default = 'False',help='include RPC', metavar='rpc')
    parser.add_option('-p','--RPCextReco', dest='RPCextReco', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-t','--RPCintReco', dest='RPCintReco', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-g','--CEGen', dest='CEGen', default = 'CEGen.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-l','--DIOGen', dest='DIOGen', default = 'DIOGen.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-k','--RPCextGen', dest='RPCextGen', default = 'RPCGen.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-u','--RPCintGen', dest='RPCintGen', default = 'RPCGen.root',help='NTuple with RPC', metavar='Rpcdir')
    #TODO - add in RPC and Cosmics
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
