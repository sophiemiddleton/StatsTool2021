#!/usr/bin/python
# Author: S Middleton
# Date: 2020
# Purpose: For exotic mu-->e+X study


import sys
import math
import numpy
import ROOT
from ROOT import TMath, TH1F, TF1, TCanvas
from Histograms import *
from Results import ResultsMu2eX
from DIO import DIO
from Mu2eX import Mu2eX
from StatsFunctions import *

class YieldFunctions:

        def __init__(self,histos, nbins, mom_low, mom_high):
            self.momentum_lower_limit = mom_low
            self.momentum_upper_limit = mom_high
            self.nBins = nbins
            self.momentum_Bin_width = (mom_high - mom_low)/nbins
            self.signal_start = 103.75
            self.signal_end = 105.45
            self.livegate = 700.
            self.POT_CD3 = 3.6e20
            self.POT_Run1 = 3.76e19
            self.capturesperStop = 0.609
            self.decaysperStop = 0.391
            self.muonstopsperPOT = 0.00159
            self.Mu2eXBR = 5e-5 #current limit
            self.sim_mu2ex_eff = 0.85
            self.sim_dio_eff = 0.5
            self.Histos = histos
            self.Results = []
            self.DIO = DIO()
            self.Mu2eX = Mu2eX()

        def MomLowLimit(self):
            return self.momentum_lower_limit

        def MomHighLimit(self):
            return self.momentum_upper_limit

        def NBins(self):
            return self.nBins

        def NBinsSetps(self):
            return (self.MomHighLimit()-self.MomLowLimit())/self.NBins()

        def MomBinWidth(self):
            return self.momentum_Bin_width

        def SignalRegionStart(self):
            return self.signal_start

        def SignalRegionEnd(self):
            return self.signal_end


        def GetPOT(self):
            return self.POT_CD3

        def GetPOTRun1(self):
            return self.POT_Run1

        def CapturesPerStop(self):
            return self.capturesperStop

        def MuonStopsPerPOT(self):
            return self.muonstopsperPOT

        def DecaysPerStop(self):
            return self.decaysperStop

        def Mu2eXBF(self):
            return self.Mu2eXBR

        def GetMu2eXSimEff(self):
            return self.sim_mu2ex_eff

        def GetDIOSimEff(self):
            return self.sim_dio_eff

        def GetIntegral(self, histo, mom_low, mom_high):
            # Translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth()) + 1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth()) + 1
            return histo.Integral(bin_low,bin_high)

        def GetN(self, histo, mom_low, mom_high):
            Nrec = self.GetIntegral(histo, mom_low, mom_high)
            return Nrec

        def GetNError(self, histo, mom_low,  mom_high):
            Nrec_error = 0
            # compute error from sum of weigths in the bins
            # translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth())+1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth())+1
            temp_error_sum = 0
            for i in range(bin_low, bin_high):
                temp_error_sum += pow(histo.GetBinError(i), 2)
            Nrec_error = math.sqrt(temp_error_sum)
            return Nrec_error

        def GetRecoEff(self, Nrec, Ngen):
            efficiency = Nrec / Ngen
            return efficiency

        def GetRecoEffError(self, Nrec, Ngen):
            """
            use Glen Cowan derivation of efficiency error based on a binomial distribution
            http://www.pp.rhul.ac.uk/~cowan/stat/notes/efferr.pdf
            """
            efficiency_error = math.sqrt(Nrec * (1. - Nrec/Ngen)) / Ngen
            return efficiency_error

        def GetExpectedYield(self, mom_low, mom_high, eff):
            N_expected = self.GetPOT() * self.MuonStopsPerPOT() * self.Mu2eXBF() * self.CapturesPerStop() * eff
            N_expected_error = 0 #TODO
            return N_expected, N_expected_error

        def GetIntegral(self, histo, mom_low, mom_high):
            # Translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth()) + 1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth()) + 1
            return histo.Integral(bin_low,bin_high)

        def GetN(self, histo, mom_low, mom_high):
            Nrec = self.GetIntegral(histo, mom_low, mom_high)
            return Nrec

        def GetNError(self, histo, mom_low,  mom_high):
            Nrec_error = 0
            # compute error from sum of weigths in the bins
            # translate mom_low and mom_up in bin numbers
            bin_low = TMath.Nint((mom_low - self.MomLowLimit()) / self.MomBinWidth())+1
            bin_high = TMath.Nint((mom_high - self.MomLowLimit()) / self.MomBinWidth())+1
            temp_error_sum = 0
            for i in range(bin_low, bin_high):
                temp_error_sum += pow(histo.GetBinError(i), 2)
            Nrec_error = math.sqrt(temp_error_sum)
            return Nrec_error

        def GetRecoEff(self, Nrec, Ngen, simeff):
            efficiency = (Nrec/simeff) / Ngen
            print("rec, gen", Nrec,Ngen)
            return efficiency

        def GetRecoEffError(self, Nrec, Ngen):
            """
            use Glen Cowan derivation of efficiency error based on a binomial distribution
            http://www.pp.rhul.ac.uk/~cowan/stat/notes/efferr.pdf
            """
            efficiency_error = math.sqrt(Nrec * (1. - Nrec/Ngen)) / Ngen
            return efficiency_error

        def GetDIOEffError(self, Nrec, Nrec_error, Ngen, Ngen_error):
            efficiency_error = math.sqrt( pow(Nrec_error / Ngen, 2) + pow( Nrec * Ngen_error / (Ngen*Ngen), 2) )
            return efficiency_error

        def GetSignalExpectedYield(self, efficiency_mu2eX):
            BF_assumption = 5e-5
            N_Mu2eX_expected = self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * BF_assumption * efficiency_mu2eX
            return N_Mu2eX_expected

        def GetSES(self, efficiency_mu2eX):
            # calculate single event sensitivity (SES), corresponds to branching fraction where 1 signal event is observed
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_mu2eX  )
            print(self.GetPOT() , self.MuonStopsPerPOT() , self.CapturesPerStop() , efficiency_mu2eX)
            return SES

        def GetSESError(self, efficiency_mu2eX, efficiency_error_mu2eX):
            # calculate error of single event sensitivity (SES),
            #corresponds to unMu2eXrtainting on branching fraction where 1 signal event is observed
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * pow(efficiency_mu2eX, 2) ) * efficiency_error_mu2eX  # error propagation on SES calculation
            return SES

        def GetDIOExpectedYield(self, N_DIO_rec, N_DIO_gen, efficiency_error_DIO, mom_low, mom_high):
            CzerneckiIntegral = self.DIO.GetInt(mom_low, mom_high)
            print("Interngral", CzerneckiIntegral)
            N_DIO_expected = N_DIO_rec * CzerneckiIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() / N_DIO_gen
            N_DIO_expected_error = CzerneckiIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() * efficiency_error_DIO
            # compute error on N_DIO_expected from error on the efficiency
            if (abs(mom_low - self.SignalRegionStart()) < 0.01 and abs(mom_high - self.SignalRegionEnd()) < 0.01):
                print( "===========================================================================")
                print( "N_DIO_rec = " , N_DIO_rec )
                print( "N_DIO_gen = " , N_DIO_gen )
                print( "Czernecki Integral = " , CzerneckiIntegral )
                print( "N_DIO_expected = " , N_DIO_expected )
                print( "N_DIO_expected_error = " , N_DIO_expected_error)
            print(N_DIO_rec,CzerneckiIntegral ,self.GetPOT(),self.MuonStopsPerPOT(),self.DecaysPerStop() , N_DIO_gen, N_DIO_expected)
            return N_DIO_expected, N_DIO_expected_error

        def GetMu2eXExpectedYield(self, N_Mu2eX_rec, N_Mu2eX_gen, efficiency_error_Mu2eX, mom_low, mom_high):
            Mu2eXIntegral = self.Mu2eX.GetInt(mom_low, mom_high)
            N_Mu2eX_expected = N_Mu2eX_rec * Mu2eXIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() / N_Mu2eX_gen
            N_Mu2eX_expected_error = Mu2eXIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() * efficiency_error_Mu2eX
            # compute error on N_DIO_expected from error on the efficiency
            if (abs(mom_low - self.SignalRegionStart()) < 0.01 and abs(mom_high - self.SignalRegionEnd()) < 0.01):
                print( "===========================================================================")
                print( "N_Mu2eX_rec = " , N_Mu2eX_rec )
                print( "N_Mu2eX_gen = " , N_Mu2eX_gen )
                print( "Czernecki Integral = " , Mu2eXIntegral )
                print( "N_Mu2eX_expected = " , N_Mu2eX_expected )
                print( "N_Mu2eX_expected_error = " , N_Mu2eX_expected_error)
            print(N_Mu2eX_rec, Mu2eXIntegral ,self.GetPOT(),self.MuonStopsPerPOT(),self.DecaysPerStop() , N_Mu2eX_gen, N_Mu2eX_expected)
            return N_Mu2eX_expected, N_Mu2eX_expected_error



        def GetBFUL(self, Nsig_UL, efficiency_mu2eX):
            BF_upper_limit = Nsig_UL / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_mu2eX )
            return BF_upper_limit

        def GetBFULError(self, Nsig_UL, Nsig_UL_error, efficiency_mu2eX, efficiency_error_mu2eX):
            BF_upper_limit_error = 1. / (self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop()) * math.sqrt(pow(Nsig_UL_error/efficiency_mu2eX, 2)
            + pow(Nsig_UL * efficiency_error_mu2eX/(efficiency_mu2eX*efficiency_mu2eX), 2))
            return BF_upper_limit_error

        def GetSingleResult(self, mom_low, mom_high, use_offline):
            result = ResultsMu2eX()
            stats = StatsFunctions()
            result.momentum_low = mom_low
            result.momentum_high = mom_high

            if use_offline == True:
                result.N_Mu2eX_gen =  self.Histos.histo_Mu2eX_generated.GetEntries()
                result.N_Mu2eX_rec = self.GetN(self.Histos.histo_Mu2eX_reconstructed , mom_low, mom_high)
                result.efficiency_Mu2eX = self.GetRecoEff(result.N_Mu2eX_rec,result.N_Mu2eX_gen, self.GetMu2eXSimEff())
                result.efficiency_error_Mu2eX = self.GetRecoEffError(result.N_Mu2eX_rec,result.N_Mu2eX_gen)
                result.N_Mu2eX_expected = self.GetSignalExpectedYield(result.efficiency_Mu2eX) #self.GetMu2eXExpectedYield(result.N_Mu2eX_rec, result.N_Mu2eX_rec_error, result.N_Mu2eX_gen, result.N_Mu2eX_gen_error) #s
                result.N_Mu2eX_expected_error = self.GetSignalExpectedYield(result.efficiency_error_Mu2eX)
            if use_offline == False:
                result.N_Mu2eX_gen =  self.GetN(self.Histos.histo_Mu2eX_generated_reweighted, mom_low, mom_high)
                result.N_Mu2eX_rec = self.GetN(self.Histos.histo_Mu2eX_reconstructed_reweighted , mom_low, mom_high)
                result.efficiency_Mu2eX = self.GetRecoEff(result.N_Mu2eX_rec,result.N_Mu2eX_gen, self.GetMu2eXSimEff())
                result.efficiency_error_Mu2eX = self.GetRecoEffError(result.N_Mu2eX_rec,result.N_Mu2eX_gen)
                result.N_Mu2eX_expected, result.N_Mu2eX_expected_error  = self.GetMu2eXExpectedYield(result.N_Mu2eX_rec,result.N_Mu2eX_gen, result.efficiency_error_Mu2eX,mom_low, mom_high)

            result.SES = self.GetSES(result.efficiency_Mu2eX)
            result.SES_error =  self.GetSESError(result.efficiency_Mu2eX,result.efficiency_error_Mu2eX)
            result.N_DIO_gen = self.GetN(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high)
            result.N_DIO_gen_error = self.GetNError(self.Histos.histo_DIO_generated_reweighted,mom_low, mom_high)
            result.N_DIO_rec = self.GetN(self.Histos.histo_DIO_reconstructed_reweighted , mom_low, mom_high)
            result.efficiency_DIO = self.GetRecoEff(result.N_DIO_rec,result.N_DIO_gen, self.GetDIOSimEff())
            result.N_DIO_rec = result.N_DIO_rec/self.GetDIOSimEff()
            result.N_DIO_rec_error = self.GetNError(self.Histos.histo_DIO_reconstructed_reweighted, mom_low, mom_high)

            result.efficiency_error_DIO = self.GetDIOEffError(result.N_DIO_rec, result.N_DIO_rec_error, result.N_DIO_gen, result.N_DIO_gen_error);
            result.N_DIO_expected, result.N_DIO_expected_error = self.GetDIOExpectedYield(result.N_DIO_rec,result.N_DIO_gen, result.efficiency_error_DIO,mom_low, mom_high)
            if(result.N_DIO_expected > 9):
                result.N_DIO_expected = 9
            result.Nsig_UL = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected)
            #result.Nsig_UL_error = 999
            #if (result.Nsig_UL != 999):

            temp_Nsig_UL_error_lower = result.Nsig_UL - stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected - result.N_DIO_expected_error) #TODO - add RPC/Cosmics
            temp_Nsig_UL_error_upper = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected + result.N_DIO_expected_error) - result.Nsig_UL
            result.Nsig_UL_error = max(temp_Nsig_UL_error_lower, temp_Nsig_UL_error_upper) # take maximum of errors to avoid asymmetric errors on Nsig_UL

            if(result.efficiency_Mu2eX !=0 and result.efficiency_error_Mu2eX!=0):
                result.BF_UL = self.GetBFUL(result.Nsig_UL,result.efficiency_Mu2eX);
                result.BF_UL_error = self.GetBFULError(result.Nsig_UL,result.Nsig_UL_error,result.efficiency_Mu2eX,result.efficiency_error_Mu2eX);
            result.PrintResultsMu2eX()

        def FillResults(self):
            mom_low=self.MomLowLimit()
            stats = StatsFunctions()
            Ngen_Mu2eX = self.Histos.histo_Mu2eX_generated.GetEntries()
            while(mom_low < self.MomHighLimit()):
                mom_high = mom_low + 0.05
                while(mom_high < self.MomHighLimit()):
                    print("Evaluating", mom_low, mom_high)
                    #perform calculations, check results for reasanable values and for infinity or NaN, save results
                    result = ResultsMu2eX()
                    result.momentum_low = mom_low
                    if (math.isnan(result.momentum_low)):
                        break
                    result.momentum_high = mom_high
                    if (math.isnan(result.momentum_high)):
                        break

                    result.N_Mu2eX_gen =  self.Histos.histo_Mu2eX_generated.GetEntries()
                    if (math.isnan(result.N_Mu2eX_gen)):
                        break

                    result.N_Mu2eX_rec = self.GetN(self.Histos.histo_Mu2eX_reconstructed, mom_low,mom_high)
                    if (math.isnan(result.N_Mu2eX_rec)):
                        break

                    if(result.N_Mu2eX_gen !=0):
                        result.efficiency_Mu2eX = self.GetRecoEff(result.N_Mu2eX_rec,result.N_Mu2eX_gen, self.GetMu2eXSimEff())
                    else:
                        result.efficiency_Mu2eX = 1
                    if (math.isnan(result.efficiency_Mu2eX)):
                         break

                    if(result.N_Mu2eX_gen !=0):
                        result.efficiency_error_Mu2eX = self.GetRecoEffError(result.N_Mu2eX_rec,result.N_Mu2eX_gen)
                    else :
                        result.efficiency_error_Mu2eX = 1
                    if (math.isnan(result.efficiency_error_Mu2eX) or result.N_Mu2eX_gen == 0):
                        break

                    result.N_Mu2eX_expected = self.GetSignalExpectedYield(result.efficiency_Mu2eX)
                    if (math.isnan(result.N_Mu2eX_expected)):
                        break

                    result.N_Mu2eX_expected_error = self.GetSignalExpectedYield(result.efficiency_error_Mu2eX)
                    if (math.isnan(result.N_Mu2eX_expected_error)):
                        break

                    result.N_DIO_gen = self.GetN(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high); # use same function as for reconstructed DIOs to integrate histograms
                    if (math.isnan(result.N_DIO_gen)):
                        break
                    if(result.N_DIO_gen == 0):
                        break
                    print("Results.N_DIO_gen = ",result.N_DIO_gen)

                    result.N_DIO_gen_error = self.GetNError(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high)
                    if (math.isnan(result.N_DIO_gen_error)):
                        break
                    result.N_DIO_rec = self.GetN(self.Histos.histo_DIO_reconstructed_reweighted , mom_low, mom_high)
                    result.N_DIO_rec = result.N_DIO_rec/self.GetDIOSimEff()
                    if (math.isnan(result.N_DIO_rec)):
                        break

                    print("Result.N_DIO_rec = ",result.N_DIO_rec)

                    result.N_DIO_rec_error = self.GetNError(self.Histos.histo_DIO_reconstructed_reweighted, mom_low, mom_high)
                    if (math.isnan(result.N_DIO_rec_error)):
                        break

                    result.efficiency_DIO = self.GetRecoEff(result.N_DIO_rec,result.N_DIO_gen, 1)
                    if (math.isnan(result.efficiency_DIO)):
                        break

                    result.efficiency_error_DIO = self.GetDIOEffError(result.N_DIO_rec, result.N_DIO_rec_error, result.N_DIO_gen, result.N_DIO_gen_error);
                    if (math.isnan(result.efficiency_error_DIO)):
                        break

                    result.N_DIO_expected, result.N_DIO_expected_error = self.GetDIOExpectedYield(result.N_DIO_rec,result.N_DIO_gen, result.efficiency_error_DIO, mom_low,mom_high);
                    if (math.isnan(result.N_DIO_expected)):
                        break

                    if(result.efficiency_Mu2eX!=0):
                        result.SES = self.GetSES(result.efficiency_Mu2eX)
                        result.SES_error =  self.GetSESError(result.efficiency_Mu2eX,result.efficiency_error_Mu2eX)
                    else:
                        result.SES = 0
                        result.SES_error =  0
                    if (math.isnan(result.SES) or math.isnan(result.SES_error)):
                        break
                    if(result.N_DIO_expected > 10):
                        result.N_DIO_expected = 10
                    result.Nsig_UL = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected) #TODO + result.N_intRPCs_expected + result.N_extRPCs_expected)
                    if (math.isnan(result.Nsig_UL)):
                        break
                    print("Expected DIO", result.N_DIO_expected , result.N_DIO_expected_error, result.Nsig_UL)
                    # calculate error on Nsig_UL by calculation of the Feldman-Cousins sensitivity of N_DIO_expected - 1*sigma and N_DIO_expected + 1*sigma, take maximum of both values
                    result.Nsig_UL_error = 999
                    if(result.N_DIO_expected > 9):
                        result.N_DIO_expected = 9
                    if (result.Nsig_UL != 999):

                        temp_Nsig_UL_error_lower = result.Nsig_UL - stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected - result.N_DIO_expected_error)
                        temp_Nsig_UL_error_upper = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected + result.N_DIO_expected_error) - result.Nsig_UL
                        result.Nsig_UL_error = max(temp_Nsig_UL_error_lower, temp_Nsig_UL_error_upper) # take maximum of errors to avoid asymmetric errors on Nsig_UL

                    if(result.efficiency_Mu2eX !=0 and result.Nsig_UL!=999):
                        result.BF_UL = self.GetBFUL(result.Nsig_UL, result.efficiency_Mu2eX);
                    if(result.efficiency_error_Mu2eX !=0 and result.Nsig_UL!=999):
                        result.BF_UL_error = self.GetBFULError(result.Nsig_UL,result.Nsig_UL_error,result.efficiency_Mu2eX,result.efficiency_error_Mu2eX);

                    if (math.isnan(result.BF_UL_error)):
                        break
                    print("BFUL", result.BF_UL)
                    if (math.isnan(result.BF_UL)):
                        break

                    result.optimal_window = 0
                    self.Results.append(result)
                    mom_high += self.momentum_Bin_width
                mom_low += self.momentum_Bin_width
            for i, j in enumerate(self.Results):
                print("=============================")
                print(i)
                j.PrintResultsMu2eX()

            # iterate over results_vector and find the optimal window with respect to the 90% Feldman-Cousins BF upper limit
            temp_index = -1
            temp_BF_UL = 999
            for i, j in enumerate(self.Results):
                if (self.Results[i].BF_UL < temp_BF_UL and self.Results[i].BF_UL!=0):
                    temp_index = i
                    temp_BF_UL = self.Results[i].BF_UL

            self.Results[temp_index].optimal_window=1 # set flag to 1 for the entry with the optimal window
            print("Optimal")
            self.Results[temp_index].PrintResultsMu2eX()

        def WriteHistograms(self):
            """function to make TTree"""
            c_dio = TCanvas()
            c_dio.Divide(2,2)
            c_dio.cd(1)
            self.Histos.histo_DIO_generated_reweighted.Draw('HIST')
            c_dio.cd(2)
            self.Histos.histo_DIO_reconstructed_reweighted.Draw('HIST')
            c_dio.SaveAs("DIO.Mu2eX.root")

            c_signal=TCanvas()
            c_signal.Divide(2,2)
            c_signal.cd(1)
            self.Histos.histo_Mu2eX_generated.Draw('HIST')
            c_signal.cd(2)
            self.Histos.histo_Mu2eX_reconstructed.Draw('HIST')
            c_signal.SaveAs("Mu2eX.root")

            outHistFile = ROOT.TFile.Open("DIOReweight.root" ,"RECREATE")
            outHistFile.cd()

            self.Histos.histo_DIO_reconstructed_reweighted.Write()

            outHistFile.Close()
