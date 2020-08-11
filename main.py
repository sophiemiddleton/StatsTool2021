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
import StatsFunctions

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
    print("Importing Data from: ", options.CE, " and", options.DIO)
    data = ImportData(options.CE, options.DIO)
    histos = Histograms(400, 90., 110.)

    DIO_reco_mom = data.GetFeature( "DIO", "deent.mom")
    CE_reco_mom = data.GetFeature( "CE", "deent.mom")
    histos.FillHistogram(histos.histo_CE_reconstructed , CE_reco_mom)
    histos.FillHistogram(histos.histo_DIO_reconstructed_flat , DIO_reco_mom)

    DIO_gen_momTot = data.GetMagFeature("DIO", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    CE_gen_momTot = data.GetMagFeature("CE", "demcgen.momx", "demcgen.momx", "demcgen.momx")
    histos.FillHistogram(histos.histo_CE_generated , CE_gen_momTot)
    histos.FillHistogram(histos.histo_DIO_generated_flat , DIO_gen_momTot)

    stats = StatsFunctions(histos)
    #plot1DHist(options.CE, "TrkAnaNeg", "trkana", "deent.mom")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CE', dest='CE', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-o','--DIO', dest='DIO', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    #TODO - add in RPC and Cosmics
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);
    print("Finished")
