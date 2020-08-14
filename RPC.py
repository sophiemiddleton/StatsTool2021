# Author: S Middleton
# Data : 2020
# Description : Hold info for RPC calculations

import sys
import uproot
import math
import pandas

class RPC() :

    def __init__(self, histos):
        self.process = "RPC"
        self.POT = 1e8
        self.frpc = 0.0215
        self.rhoRPC = 0.0069
        self.psurv = 1.
        self.reco_eff = 1.
        self.sumPionWeights = 0
        self.pionsStopped = 0
        self.RPCintHist = histos.histo_intRPC_reconstructed
        self.RPCextHist = histos.histo_extRPC_reconstructed
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

    def GetRPCEff(self, genRPC, type, max, min):
        if type == "internal":
            self.reco_eff = self.RPCintHist.GetIntegral(min,max)/(self.sumPionWeights*(genRPC/self.pionsStopped))
        if type == "external":
            self.reco_eff = self.RPCextHist.GetIntegral(min, max)/(self.sumPionWeights*(genRPC/self.pionsStopped))
        return self.reco_eff
