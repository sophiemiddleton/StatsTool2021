# Author : S Middleton
# Date : 2021
# Purpose : Stores optional cuts

import sys

class Cuts() :

    def __init__(self, opt = 'su2020', use_CRV = False):
        self.use_CRV = use_CRV
        self.Cut_List = {}
        if opt is 'cd3':
            self.Cut_List =  {
                  "de.status" : [0., float("inf")] ,  #goodfit
                  "trigbits&0x208" : [0., float("inf")], #triggered
                  "de.t0" : [700., 1695],    #inTimeWindow
                  "deent.td" : [0.577350, 1.000],    #inTanDipCut
                  "deent.d0" : [-80., 105.], #inD0Cut
                  "inMaxRCut" : [450., 680.],
                  "useCRV"  : use_CRV,
                  "noCRVHit" : [-50.0 , 150.0],
                  "dequal.TrkQual" : [0.8, float("inf")],  #TrkQual
                  "dequal.TrkPID" : [0.95, float("inf")],  #TrkPID
                  "ue.status" : [float("-inf"), 0.],   #noUpstream
                  "deent.mom" : [95., float("inf")]   #recomom

                }

        if opt is 'su2020':
                self.Cut_List =  {
                      "de.t0" : [700., 1695],    #inTimeWindow
                      "deent.td" : [0.5, 1.0],    #inTanDipCut
                      "deent.d0" : [-100,100.], #inD0Cut
                      "dequal.TrkQual" : [0.2, float("inf")],  #TrkQual
                    }

    def ApplyCut(self, df):
        df_cut = df
        for key, value in self.Cut_List.items():
            df_cut = df_cut[(df_cut[key] > value[0]) & (df_cut[key] <= value[1])]
        return df_cut
