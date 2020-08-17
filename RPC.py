# Author: S Middleton
# Data : 2020
# Description : Hold info for RPC calculations

import sys
import uproot
import math
import pandas

class RPC() :

    def __init__(self, histos,intfile,extfile, min, max, livegate, treename="TrkAnaNeg", branchname="trkana"):
        self.process = "RPC"
        self.POT = 1e8
        self.frpc = 0.0215
        self.rhoRPC = 0.0069
        self.psurv = 1.
        self.reco_eff = 1.
        self.sumPionWeights = 0
        self.pionsStopped = 0
        self.SumofSigWeightsInt = 0
        self.SumofSigWeightsExt = 0
        self.RecoEffInt = 0
        self.RecoEffExt = 0
        self.Ngen_int  = 1e8
        self.Ngen_ext = 1e9
        # Fill Sums in Signal Regions:

        input_file_int = uproot.open(intfile)
        input_tree_int = input_file_int[treename][branchname]
        df_int = input_tree_int.pandas.df(flatten=False)
        for k,l in enumerate(df_int["deent.mom"]):
            if l>min and l <max and df_int["de.t0"][k]>livegate:
                self.SumofSigWeightsInt += df_int["evtwt.generate"][k]
        input_file_ext = uproot.open(extfile)
        input_tree_ext = input_file_int[treename][branchname]
        df_ext = input_tree_ext.pandas.df(flatten=False)
        for k,l in enumerate(df_ext["deent.mom"]):
            if l>min and l <max and df_ext["de.t0"][k]>livegate:
                self.SumofSigWeightsExt += df_ext["evtwt.generate"][k]
        print(self.SumofSigWeightsInt, self.SumofSigWeightsExt)

        # Extract Pion Weights:
        file = uproot.open("../RPC/pions.root")
        Pions = file["stoppedPionDumper;1"]["StoppedPions;1"]
        df = Pions.pandas.df(flatten=False)
        for i,j in enumerate(df["StoppedPions.time"]):
            weight = math.exp(-j/26)
            self.sumPionWeights += weight
            self.pionsStopped +=1
        print("Stopped Pions:", self.pionsStopped, "Sum of Weights:", self.sumPionWeights)

    def SumPionWeights(self):
        self.sumPionWeights = 0
        file = uproot.open("../RPC/pions.root")
        Pions = file["stoppedPionDumper;1"]["StoppedPions;1"]
        df = Pions.pandas.df(flatten=False)
        for i,j in enumerate(df["StoppedPions.time"]):
            weight = math.exp(-j/26)
            self.sumPionWeights += weight
        print(self.sumPionWeights)

    def PionStopsPerPOT(self):
        return self.pionsStopped/self.POT

    def RhoIntRPC(self):
        return self.frpc

    def RPCBF(self):
        return self.rhoRPC

    def PionPsurv(self):
        self.psurv = self.sumPionWeights/self.pionsStopped
        return self.psurv

    def GetRPCEffInt(self, genRPC):
        self.reco_eff = self.SumofSigWeightsInt/(self.sumPionWeights*(genRPC/self.pionsStopped))
        return self.RecoEffInt

    def GetRPCEffExt(self, genRPC):
        self.reco_eff = self.SumofSigWeightsExt/(self.sumPionWeights*(genRPC/self.pionsStopped))
        return self.RecoEffExt

    def GetGenExt(self):
        return self.Ngen_ext

    def GetGenInt(self):
        return self.Ngen_int
