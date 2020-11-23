# Resolution - is modelled by double sided crystal ball function
import ROOT
import uproot
import math
from ROOT import TMath, TCanvas, TH1F, TText, TLatex, TF1
import pandas

class Resolution_Func :

    def __init__(self, filename):
        self.filename = filename

    def fnc_dscb(self, xx,pp):
        x   = xx[0]

        N   = pp[0]
        mu  = pp[1]
        sig = pp[2]

        a1  = pp[3]
        p1  = pp[4]
        a2  = pp[5]
        p2  = pp[6]

        u   = (x-mu)/sig
        A1  = TMath.Power(p1/TMath.Abs(a1),p1)*TMath.Exp(-a1*a1/2)
        A2  = TMath.Power(p2/TMath.Abs(a2),p2)*TMath.Exp(-a2*a2/2)
        B1  = p1/TMath.Abs(a1) - TMath.Abs(a1)
        B2  = p2/TMath.Abs(a2) - TMath.Abs(a2)

        result = N
        if(u<-a1):
            result *= A1*TMath.Power(B1-u,-p1)
        if(u<a2):
            result *= TMath.Exp(-u*u/2)
        else:
            result *= A2*TMath.Power(B2+u,-p2)
        return result

    def Fit_Resolution(self):

        h = ROOT.TH1F("Resolution",  "Momentum Reosolution", 100, -2,2)

        file = uproot.open(self.filename)
        RPCReco = file["TrkAnaNeg"]["trkana"]
        df = RPCReco.pandas.df(flatten=False)

        for i,j in enumerate(df["deent.mom"]):
            momGen = math.sqrt(df["demcent.momx"][i]**2 + df["demcent.momy"][i]**2 + df["demcent.momz"][i]**2)
            h.Fill(j - momGen)


            c = ROOT.TCanvas("myCanvasName","The Canvas Title",800,600)
            h.Draw()
            c.Draw()
            n_parameters = 7;
            dscb = ROOT.TF1("dscb", self.fnc_dscb, -2, 4, n_parameters);
            dscb.SetParName(0,"Norm");
            dscb.SetParName(1,"x0");
            dscb.SetParName(2,"sigma");
            dscb.SetParName(3,"ANeg");
            dscb.SetParName(4,"PNeg");
            dscb.SetParName(5,"APos");
            dscb.SetParName(6,"PPos");
            integral = h.Integral();
            dscb.SetParameters(integral, h.GetMean(),0.5*h.GetRMS(),0.9,3.5,1.1,6.0);
            h.Fit("dscb", "LR");

            c.Draw()
            h.GetXaxis().SetTitle("Electron Momentum [MeV/c]")
            h.GetYaxis().SetTitle("Weighted N")
            c.SaveAs("Resolution.root")
