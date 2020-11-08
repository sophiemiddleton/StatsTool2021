#!/usr/bin/python
import argparse
import importlib
import ROOT
from ROOT import TTree, TBranch
ROOT.gSystem.Load("/nfs/slac/g/ldmx/users/smidd/NewLDMX/v2.3/ldmx-sw/install/lib/libEvent.so")
import os
import math
import sys
#import numpy as np
import matplotlib.pyplot as plt
from array import array
from optparse import OptionParser
sys.path.insert(0, '../')


class Event():
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.e = []
        self.pid = []

class WabEvent:

    def __init__(self, fn1, ofn, tag):

        self.fin1 = ROOT.TFile(fn1);
        self.tin1 = self.fin1.Get("LDMX_Events")

        self.tag = int(tag);

        self.fn_out = ofn;
        self.fout = ROOT.TFile("hist_"+self.fn_out,"RECREATE");

        #wab:
        self.evHeader1 = ROOT.ldmx.EventHeader()
        self.simParticles1 = ROOT.std.map(int,'ldmx::SimParticle')();
        self.hcalHits1 = ROOT.std.vector('ldmx::HcalHit')();
        self.ecalHits1 = ROOT.std.vector('ldmx::EcalHit')();
        self.hcalSimHits1 = ROOT.std.vector('ldmx::SimCalorimeterHit')();
        self.recoilSimHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.hcalScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.ecalScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.targetScoringPlaneHits1 = ROOT.std.vector('ldmx::SimTrackerHit')();
        self.tin1.SetBranchAddress("EventHeader",  ROOT.AddressOf( self.evHeader1 ));
        self.tin1.SetBranchAddress("HcalSimHits_v12",  ROOT.AddressOf( self.hcalSimHits1 ));
        self.tin1.SetBranchAddress("RecoilSimHits_v12",  ROOT.AddressOf( self.recoilSimHits1 ));
        self.tin1.SetBranchAddress("HcalRecHits_v12",  ROOT.AddressOf( self.hcalHits1 ));
        self.tin1.SetBranchAddress("EcalRecHits_v12",  ROOT.AddressOf( self.ecalHits1 ));
        self.tin1.SetBranchAddress("HcalScoringPlaneHits_v12",  ROOT.AddressOf(self.hcalScoringPlaneHits1));
        self.tin1.SetBranchAddress("EcalScoringPlaneHits_v12",  ROOT.AddressOf(self.ecalScoringPlaneHits1));
        self.tin1.SetBranchAddress("TargetScoringPlaneHits_v12",  ROOT.AddressOf(self.targetScoringPlaneHits1));
        self.tin1.SetBranchAddress("SimParticles_v12",  ROOT.AddressOf( self.simParticles1 ));

        self.SumHCAL = []
        self.RecHits_PE_ECAL = []
        self.RecHits_E_ECAL = []

        self.RecHits_PE_HCAL = []
        self.RecHits_E_HCAL = []

        self.GreenPDG = []
        self.BluePDG = []
        self.RedPDG = []
        self.PurplePDG = []
        self.YellowPDG = []

        self.loop();
        self.writeOutHistos();

    def writeOutHistos(self):

        self.fout.cd();

    def loop(self):

        nentWAB = self.tin1.GetEntriesFast();
        for i in range(nentWAB):
            sum_sim_e = 0
            self.tin1.GetEntry(i);
            for ih,hit in enumerate(self.hcalSimHits1):
                sum_sim_e += hit.getEdep();
            self.SumHCAL.append(sum_sim_e)


        for i in range(100):
            self.tin1.GetEntry(i);
            sum_sim_e = 0
            for ih,hit in enumerate(self.hcalHits1):
                 if (hit.isNoise()==0 and hit.getXPos()!=0 and hit.getYPos()!=0 and hit.getZPos()!=0):

                    sum_sim_e += hit.getPE()
                    #print(i, ih, hit.getID()& 0xFFF)
            self.RecHits_PE_HCAL.append(sum_sim_e)

            sum_sim_ecal = 0
            for ih,hit in enumerate(self.ecalHits1):
                 if (hit.isNoise()==0 and hit.getXPos()!=0 and hit.getYPos()!=0 and hit.getZPos()!=0):
                    sum_sim_ecal += hit.getEnergy()
            self.RecHits_E_ECAL.append(sum_sim_ecal)

            for ih,hit in enumerate(self.hcalHits1):
                 if (hit.isNoise()==0 and hit.getXPos()!=0 and hit.getYPos()!=0 and hit.getZPos()!=0):
                    for ik,simhit in enumerate(self.hcalSimHits1):
                        if hit.getID()== simhit.getID():
                            for n in  range(0,simhit.getNumberOfContribs()):
                                contrib = simhit.getContrib(n)
                                #print("simhit has", simhit.getNumberOfContribs(), "PDGis", contrib.pdgCode)
                                if(sum_sim_e<2000):
                                    for ij,ecalhit in enumerate(self.ecalHits1):
                                        if (ecalhit.isNoise()==0 and ecalhit.getXPos()!=0 and ecalhit.getYPos()!=0 and ecalhit.getZPos()!=0):
                                            if(sum_sim_ecal<1500):
                                                self.GreenPDG.append(abs(contrib.pdgCode))
                                if(sum_sim_e<4000 and sum_sim_e>2000):
                                    for ij,ecalhit in enumerate(self.ecalHits1):
                                        if (ecalhit.isNoise()==0 and ecalhit.getXPos()!=0 and ecalhit.getYPos()!=0 and ecalhit.getZPos()!=0):
                                            if(sum_sim_ecal<1000):
                                                self.BluePDG.append(abs(contrib.pdgCode))
                                if(sum_sim_e<7000 and sum_sim_e>5000):
                                    for ij,ecalhit in enumerate(self.ecalHits1):
                                        if (ecalhit.isNoise()==0 and ecalhit.getXPos()!=0 and ecalhit.getYPos()!=0 and ecalhit.getZPos()!=0):
                                            if(sum_sim_ecal<1000):
                                                print(contrib.pdgCode)
                                                self.YellowPDG.append(abs(contrib.pdgCode))
                                if(sum_sim_e<2000):
                                    for ij,ecalhit in enumerate(self.ecalHits1):
                                        if (ecalhit.isNoise()==0 and ecalhit.getXPos()!=0 and ecalhit.getYPos()!=0 and ecalhit.getZPos()!=0):
                                            if(sum_sim_ecal<3000 and sum_sim_ecal>2000):
                                                self.RedPDG.append(abs(contrib.pdgCode))
                                if(sum_sim_e>3500):
                                    for ij,ecalhit in enumerate(self.ecalHits1):
                                        if (ecalhit.isNoise()==0 and ecalhit.getXPos()!=0 and ecalhit.getYPos()!=0 and ecalhit.getZPos()!=0):
                                            if(sum_sim_ecal<2000 ):
                                                self.PurplePDG.append(abs(contrib.pdgCode))





def main(options,args) :
    sc = WabEvent(options.ifile1, options.ofile,options.tag) ;
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    p = ax.hist2d(x=sc.RecHits_PE_HCAL, y=sc.RecHits_E_ECAL,cmin=1, bins=100 ,cmap=plt.cm.jet)

    ax.set_xlabel('Sum of PE at HCAL' )
    ax.set_ylabel('Sum Energy Deposited at ECAL')

    plt.savefig("PEvE.png")
    """
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.GreenPDG,
            bins=25,
            range=(0,23), color='g',
            label="Green")
    ax.set_xlabel('PDG Code Green Region')
    #ax.set_yscale('log')
    plt.savefig("Green.png")

    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.BluePDG,
            bins=25,
            range=(0,23), color='b',
            label="Blue")
    ax.set_xlabel('PDG Code Blue Region')
    #ax.set_yscale('log')
    plt.savefig("Blue.png")

    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.RedPDG,
            bins=25,
            range=(0,23), color='r',
            label="Red")
    ax.set_xlabel('PDG Code Red Region')
    #ax.set_yscale('log')
    plt.savefig("Red.png")

    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.YellowPDG,
            bins=25,
            range=(0,23), color='y',
            label="Yellow")
    ax.set_xlabel('PDG Code Yellow Region')
    #ax.set_yscale('log')
    plt.savefig("Yellow.png")

    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist(sc.PurplePDG,
            bins=25,
            range=(0,23), color='g',
            label="Purple")
    ax.set_xlabel('PDG Code Purple Region')
    #ax.set_yscale('log')
    plt.savefig("Purple.png")
    sc.fout.Close();

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    # input data files (4)
    parser.add_option('-a','--ifile1', dest='ifile1', default = 'file1.root',help='directory with data1', metavar='idir1')
    parser.add_option('-o','--ofile', dest='ofile', default = 'ofile.root',help='directory to write plots', metavar='odir')
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    ROOT.gStyle.SetPadTopMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.16)
    ROOT.gStyle.SetPadRightMargin(0.10)
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("1.1f")
    ROOT.gStyle.SetOptFit(0000)
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    # Get the Event library
    ROOT.gSystem.Load("/nfs/slac/g/ldmx/users/smidd/NewLDMX/v2.3/ldmx-sw/install/lib/libEvent.so")	;

    main(options,args);
