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
from ImportData import ImportData
from Histograms import Histograms
from Functions import *
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
    print("Importing Data from: CE", options.CE, "DIO", options.DIO, "internal RPC", options.RPCint, "external RPC", options.RPCext)
    data = ImportData(options.CE, options.DIO, options.RPCext, options.RPCint)
    histos = Histograms(400, 90., 110.)
    #Get Data:
    DIO_reco_mom = data.GetFeature( "DIO", "deent.mom")
    CE_reco_mom = data.GetFeature( "CE", "deent.mom")
    RPCext_reco_mom = data.GetFeature( "RPCext", "deent.mom")
    RPCint_reco_mom = data.GetFeature( "RPCint", "deent.mom")
    RPCExternalWeights = data.GetFeature("RPCext", "evtwt.generate")
    RPCInternalWeights = data.GetFeature("RPCint", "evtwt.generate")

    # Fill Reco:
    histos.FillHistogram(histos.histo_CE_reconstructed , CE_reco_mom)
    histos.FillHistogram(histos.histo_DIO_reconstructed_flat , DIO_reco_mom)
    histos.FillHistogram(histos.histo_extRPC_reconstructed , RPCext_reco_mom)
    histos.FillHistogram(histos.histo_intRPC_reconstructed , RPCint_reco_mom)
    histos.DoDIOWeights(histos.histo_DIO_reconstructed_reweighted , DIO_reco_mom)
    
    # Fill Gen:
    DIO_gen_momTot = data.GetMagFeature("DIO", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    CE_gen_momTot = data.GetMagFeature("CE", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    RPCext_gen_momTot = data.GetMagFeature("RPCext", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    RPCint_gen_momTot = data.GetMagFeature("RPCint", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    histos.FillHistogram(histos.histo_CE_generated , CE_gen_momTot)
    histos.FillHistogram(histos.histo_DIO_generated_flat , DIO_gen_momTot)
    histos.FillHistogram(histos.histo_intRPC_generated , RPCint_gen_momTot)
    histos.FillHistogram(histos.histo_extRPC_generated , RPCext_gen_momTot)
    histos.DoDIOWeights(histos.histo_DIO_generated_reweighted , DIO_gen_momTot)
    # Build Functions:
    stats = StatsFunctions()
    yields = YieldFunctions(histos)
    # Fill Results
    yields.FillResults()
    #To make a plot: plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CE', dest='CE', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-o','--DIO', dest='DIO', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    parser.add_option('-p','--RPCext', dest='RPCext', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    parser.add_option('-t','--RPCint', dest='RPCint', default = 'RPCData.root',help='NTuple with RPC', metavar='Rpcdir')
    #TODO - add in RPC and Cosmics
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
