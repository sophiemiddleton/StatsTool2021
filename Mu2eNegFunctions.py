# Author : S Middleton
# Date : 2020
# Purpose : Stats functions

import sys
import math
import numpy
import ROOT
from ROOT import TMath, TH1F, TF1, TCanvas
from Histograms import Histograms
from Results import Results
from DIO import DIO
from RPC import RPC
from CE import CE
from StatsFunctions import *
from Constants import *

class YieldFunctions:

        def __init__(self,histos, nbins, mom_low, mom_high, rpc_filename_int, rpc_filename_ext, constants, showRPC=True):
            self.optimize_for = 'BFUL'
            self.showRPC = showRPC
            self.momentum_lower_limit = mom_low
            self.momentum_upper_limit = mom_high
            self.nBins = nbins
            self.momentum_Bin_width = (mom_high - mom_low)/nbins
            self.constants = constants
            self.Histos = histos
            self.Results = []
            self.DIO = DIO()
            self.CE = CE()
            self.RPC = RPC(self.Histos,rpc_filename_int, rpc_filename_ext, self.momentum_lower_limit,self.momentum_upper_limit, self.constants.livegate, self.constants.target)

        def MomLowLimit(self):
            return self.momentum_lower_limit

        def MomHighLimit(self):
            return self.momentum_upper_limit

        def NBins(self):
            return self.nBins

        def NBins(self):
            return (self.MomHighLimit()-self.MomLowLimit())/self.NBins()

        def MomBinWidth(self):
            return self.momentum_Bin_width

        def SignalRegionStart(self):
            return self.constants.signal_start

        def SignalRegionEnd(self):
            return self.constants.signal_end

        def GetPOT(self):
            return self.constants.POT

        def CapturesPerStop(self):
            return self.constants.capturesperStop

        def DecaysPerStop(self):
            return self.constants.decaysperStop

        def MuonStopsPerPOT(self):
            return self.constants.muonstopsperPOT

        def GetCESimEff(self):
            return self.constants.sim_ce_eff

        def GetDIOSimEff(self):
            return self.constants.sim_dio_eff

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
            # print("rec, gen", Nrec, Ngen)
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

        def GetSignalExpectedYield(self, efficiency_CE):
            # assume BF of 10E-16 and calculate expected signal for this BF
            BF_assumption = 1e-16
            N_CE_expected = self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * BF_assumption * efficiency_CE
            return N_CE_expected

        def GetSES(self, efficiency_CE):
            # calculate single event sensitivity (SES), corresponds to branching fraction where 1 signal event is observed
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_CE  )
            # print(self.GetPOT() , self.MuonStopsPerPOT() , self.CapturesPerStop() , efficiency_CE)
            return SES

        def GetSESError(self, efficiency_CE, efficiency_error_CE):
            # calculate error of single event sensitivity (SES),
            #corresponds to uncertainting on branching fraction where 1 signal event is observed
            SES = 1. / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * pow(efficiency_CE, 2) ) * efficiency_error_CE  # error propagation on SES calculation
            return SES

        def GetDIOExpectedYield(self, N_DIO_rec, N_DIO_gen, efficiency_error_DIO, mom_low, mom_high):
            CzerneckiIntegral = self.DIO.GetInt(mom_low, mom_high,self.constants.target)
            N_DIO_expected = N_DIO_rec * CzerneckiIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() / N_DIO_gen
            N_DIO_expected_error = CzerneckiIntegral * self.GetPOT() * self.MuonStopsPerPOT() * self.DecaysPerStop() * efficiency_error_DIO
            # compute error on N_DIO_expected from error on the efficiency
            #if (abs(mom_low - self.SignalRegionStart()) < 0.01 and abs(mom_high - self.SignalRegionEnd()) < 0.01):
            #    print( "===========================================================================")
            #    print( "N_DIO_rec = " , N_DIO_rec )
            #    print( "N_DIO_gen = " , N_DIO_gen )
            #    print( "Czernecki Integral = " , CzerneckiIntegral )
            #    print( "N_DIO_expected = " , N_DIO_expected )
            #    print( "N_DIO_expected_error = " , N_DIO_expected_error)
            #print(N_DIO_rec,CzerneckiIntegral ,self.GetPOT(),self.MuonStopsPerPOT(),self.DecaysPerStop() , N_DIO_gen, N_DIO_expected)
            return N_DIO_expected, N_DIO_expected_error

        def GetInternalRPCExpectedYield(self, N_RPCs_expected, N_RPCs_expected_error, mom_low, mom_high, eff):
            N_RPC_expected = self.GetPOT() * self.RPC.PionStopsPerPOT() * self.RPC.RhoIntRPC() * self.RPC.RPCBF() * self.RPC.PionPsurv() * eff
            N_RPCs_expected_error = 0
            return N_RPC_expected, N_RPCs_expected_error

        def GetExternalRPCExpectedYield(self, N_RPCs_expected, N_RPCs_expected_error, mom_low, mom_high, eff):
            N_RPC_expected = self.GetPOT() * self.RPC.PionStopsPerPOT() *  self.RPC.RPCBF() * self.RPC.PionPsurv() * eff
            N_RPCs_expected_error = 0
            return N_RPC_expected, N_RPCs_expected_error

        def GetCosmicsExpectedYield(self, eff):
            return 0., 0.

        def GetBFUL(self, Nsig_UL, efficiency_CE):
            BF_upper_limit = Nsig_UL / ( self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop() * efficiency_CE )
            return BF_upper_limit

        def GetBFULError(self, Nsig_UL, Nsig_UL_error, efficiency_CE, efficiency_error_CE):
            BF_upper_limit_error = 1. / (self.GetPOT() * self.MuonStopsPerPOT() * self.CapturesPerStop()) * math.sqrt(pow(Nsig_UL_error/efficiency_CE, 2)
            + pow(Nsig_UL * efficiency_error_CE/(efficiency_CE*efficiency_CE), 2))
            return BF_upper_limit_error

        def GetSingleResult(self, mom_low, mom_high):
            result = Results()
            stats = StatsFunctions()
            result.momentum_low = mom_low
            result.momentum_high = mom_high
            result.N_CE_gen =  self.Histos.histo_CE_generated.GetEntries() #TODO: assumes momlow and high contain all signal!
            result.N_CE_rec = self.GetN(self.Histos.histo_CE_reconstructed , mom_low, mom_high)
            result.efficiency_CE = self.GetRecoEff(result.N_CE_rec,result.N_CE_gen, self.GetCESimEff())
            result.efficiency_error_CE = self.GetRecoEffError(result.N_CE_rec,result.N_CE_gen)
            result.N_CE_expected = self.GetSignalExpectedYield(result.efficiency_CE)
            result.N_CE_expected_error = self.GetSignalExpectedYield(result.efficiency_error_CE)
            result.SES = self.GetSES(result.efficiency_CE)
            result.SES_error =  self.GetSESError(result.efficiency_CE,result.efficiency_error_CE)
            result.N_DIO_gen = self.GetN(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high)
            result.N_DIO_gen_error = self.GetNError(self.Histos.histo_DIO_generated_reweighted,mom_low, mom_high)
            result.N_DIO_rec = self.GetN(self.Histos.histo_DIO_reconstructed_reweighted , mom_low, mom_high)
            result.efficiency_DIO = self.GetRecoEff(result.N_DIO_rec,result.N_DIO_gen, self.GetDIOSimEff())
            result.N_DIO_rec = result.N_DIO_rec/self.GetDIOSimEff()
            result.N_intRPC_rec = self.GetN(self.Histos.histo_intRPC_reconstructed, mom_low, mom_high)
            result.N_intRPC_gen = self.GetN(self.Histos.histo_intRPC_generated, mom_low, mom_high)
            result.N_extRPC_rec = self.GetN(self.Histos.histo_extRPC_reconstructed,mom_low, mom_high)
            result.N_extRPC_gen = self.GetN(self.Histos.histo_extRPC_generated, mom_low, mom_high)
            result.efficiency_intRPC = self.GetRecoEff(result.N_intRPC_rec, result.N_intRPC_gen, 1)
            self.GetInternalRPCExpectedYield(result.N_intRPCs_expected, result.N_intRPCs_expected_error, mom_low, mom_high, result.efficiency_intRPC)
            result.efficiency_extRPC = self.GetRecoEff(result.N_extRPC_rec, result.N_extRPC_gen, 1)
            self.GetExternalRPCExpectedYield(result.N_extRPCs_expected, result.N_extRPCs_expected_error, mom_low, mom_high, result.efficiency_extRPC)
            result.N_DIO_rec_error = self.GetNError(self.Histos.histo_DIO_reconstructed_reweighted, mom_low, mom_high)

            result.efficiency_error_DIO = self.GetDIOEffError(result.N_DIO_rec, result.N_DIO_rec_error, result.N_DIO_gen, result.N_DIO_gen_error);
            result.N_DIO_expected, result.N_DIO_expected_error = self.GetDIOExpectedYield(result.N_DIO_rec,result.N_DIO_gen, result.efficiency_error_DIO,mom_low, mom_high)
            #if(result.N_DIO_expected > 9):
            #    result.N_DIO_expected = 9
            #result.Nsig_UL = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected)
            #result.Nsig_UL_error = 999
            #if (result.Nsig_UL != 999):
            result.Nsig_UL = stats.ROOTFeldmanCousins(result.N_DIO_expected, result.N_DIO_expected)
            temp_Nsig_UL_error_lower = result.Nsig_UL - stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected - result.N_DIO_expected_error) #TODO - add RPC/Cosmics
            temp_Nsig_UL_error_upper = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected + result.N_DIO_expected_error) - result.Nsig_UL
            result.Nsig_UL_error = max(temp_Nsig_UL_error_lower, temp_Nsig_UL_error_upper) # take maximum of errors to avoid asymmetric errors on Nsig_UL

            if(result.efficiency_CE !=0 and result.efficiency_error_CE!=0):
                result.BF_UL = self.GetBFUL(result.Nsig_UL,result.efficiency_CE);
                result.BF_UL_error = self.GetBFULError(result.Nsig_UL,result.Nsig_UL_error,result.efficiency_CE,result.efficiency_error_CE);
            result.PrintResults()

        def FillResults(self):
            mom_low=self.MomLowLimit()
            stats = StatsFunctions()
            Ngen_CE = self.Histos.histo_CE_generated.GetEntries()
            while(mom_low < self.MomHighLimit()):
                mom_high = mom_low + self.momentum_Bin_width

                while(mom_high < self.MomHighLimit()):
                    #perform calculations, check results for reasanable values and for infinity or NaN, save results
                    result = Results()
                    result.momentum_low = mom_low
                    if (math.isnan(result.momentum_low)):
                        break
                    result.momentum_high = mom_high
                    if (math.isnan(result.momentum_high)):
                        break

                    result.N_CE_gen =  self.GetN(self.Histos.histo_CE_generated, mom_low,mom_high)#self.Histos.histo_CE_generated.GetEntries()
                    if (result.N_CE_gen==0 or math.isnan(result.N_CE_gen)):
                        break

                    result.N_CE_rec = self.GetN(self.Histos.histo_CE_reconstructed, mom_low,mom_high)
                    if (math.isnan(result.N_CE_rec)):
                        break

                    if(result.N_CE_gen !=0):
                        result.efficiency_CE = self.GetRecoEff(result.N_CE_rec,result.N_CE_gen, self.GetCESimEff())
                    if(result.N_CE_gen ==0):
                        break

                    if (math.isnan(result.efficiency_CE)):
                         break

                    if(result.N_CE_gen !=0):
                        result.efficiency_error_CE = self.GetRecoEffError(result.N_CE_rec,result.N_CE_gen)
                    else :
                        result.efficiency_error_CE = 1
                    if (math.isnan(result.efficiency_error_CE)):
                        break

                    result.N_CE_expected = self.GetSignalExpectedYield(result.efficiency_CE)
                    if (math.isnan(result.N_CE_expected)):
                        break

                    result.N_CE_expected_error = self.GetSignalExpectedYield(result.efficiency_error_CE)
                    if (math.isnan(result.N_CE_expected_error)):
                        break

                    result.N_DIO_gen = self.GetN(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high); # use same function as for reconstructed DIOs to integrate histograms
                    if (math.isnan(result.N_DIO_gen)):
                        break
                    if(result.N_DIO_gen == 0):
                        break
                    #print("Results.N_DIO_gen = ",result.N_DIO_gen)

                    result.N_DIO_gen_error = self.GetNError(self.Histos.histo_DIO_generated_reweighted, mom_low, mom_high)
                    if (math.isnan(result.N_DIO_gen_error)):
                        break
                    result.N_DIO_rec = self.GetN(self.Histos.histo_DIO_reconstructed_reweighted , mom_low, mom_high)
                    result.N_DIO_rec = result.N_DIO_rec/self.GetDIOSimEff()
                    if (math.isnan(result.N_DIO_rec)):
                        break

                    #print("Result.N_DIO_rec = ",result.N_DIO_rec)
                    if(self.showRPC == True):
                        result.N_intRPC_rec = self.GetN(self.Histos.histo_intRPC_reconstructed, mom_low, mom_high)
                        if (math.isnan(result.N_intRPC_rec)):
                            break
                        #print("Result.N_intRPC_rec = ",result.N_intRPC_rec)

                        result.N_intRPC_gen = self.GetN(self.Histos.histo_intRPC_generated, mom_low, mom_high)
                        if (math.isnan(result.N_intRPC_gen)):
                            break

                        result.N_extRPC_rec = self.GetN(self.Histos.histo_extRPC_reconstructed, mom_low, mom_high)
                        if (math.isnan(result.N_extRPC_rec)):
                            break
                        #print("Result.N_extRPC_rec = ",result.N_extRPC_rec)

                        result.N_extRPC_gen = self.GetN(self.Histos.histo_extRPC_generated, mom_low, mom_high)
                        if (math.isnan(result.N_extRPC_gen)):
                            break

                        if( result.N_intRPC_gen !=0):
                            result.efficiency_intRPC = self.GetRecoEff(result.N_intRPC_rec, result.N_intRPC_gen, 1)
                        else:
                            result.efficiency_intRPC = 1

                        self.GetInternalRPCExpectedYield(result.N_intRPCs_expected, result.N_intRPCs_expected_error, mom_low, mom_high, result.efficiency_intRPC)
                        if (math.isnan(result.N_intRPCs_expected)):
                            break

                        if(result.N_extRPC_gen !=0):
                            result.efficiency_extRPC = self.GetRecoEff(result.N_extRPC_rec, result.N_extRPC_gen, 1)
                        else:
                            result.efficiency_extRPC = 1

                        self.GetExternalRPCExpectedYield(result.N_extRPCs_expected, result.N_extRPCs_expected_error, mom_low, mom_high, result.efficiency_extRPC)
                        if (math.isnan(result.N_extRPCs_expected)):
                            break

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

                    if(result.efficiency_CE!=0):
                        result.SES = self.GetSES(result.efficiency_CE)
                        result.SES_error =  self.GetSESError(result.efficiency_CE,result.efficiency_error_CE)
                    else:
                        result.SES = 0
                        result.SES_error =  0
                    if (math.isnan(result.SES) or math.isnan(result.SES_error)):
                        break
                    #if(result.N_DIO_expected > 9):
                    #    result.N_DIO_expected = 9
                    #result.Nsig_UL = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected) #TODO + result.N_intRPCs_expected + result.N_extRPCs_expected)
                    result.Nsig_UL = stats.ROOTFeldmanCousins(result.N_DIO_expected, result.N_DIO_expected)
                    if (math.isnan(result.Nsig_UL)):
                        break
                    #print("Expected DIO", result.N_DIO_expected , result.N_DIO_expected_error, result.Nsig_UL)
                    # calculate error on Nsig_UL by calculation of the Feldman-Cousins sensitivity of N_DIO_expected - 1*sigma and N_DIO_expected + 1*sigma, take maximum of both values
                    result.Nsig_UL_error = 999
                    #if(result.N_DIO_expected > 9):
                    #    result.N_DIO_expected = 9
                    if (result.Nsig_UL != 999):

                        temp_Nsig_UL_error_lower = result.Nsig_UL - stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected - result.N_DIO_expected_error)
                        temp_Nsig_UL_error_upper = stats.GetFeldmanCousinsSensitivity(result.N_DIO_expected + result.N_DIO_expected_error) - result.Nsig_UL
                        result.Nsig_UL_error = max(temp_Nsig_UL_error_lower, temp_Nsig_UL_error_upper) # take maximum of errors to avoid asymmetric errors on Nsig_UL

                    if(result.efficiency_CE !=0 and result.Nsig_UL!=999):
                        result.BF_UL = self.GetBFUL(result.Nsig_UL, result.efficiency_CE);
                    if(result.efficiency_error_CE !=0 and result.Nsig_UL!=999):
                        result.BF_UL_error = self.GetBFULError(result.Nsig_UL,result.Nsig_UL_error,result.efficiency_CE,result.efficiency_error_CE);

                    if (math.isnan(result.BF_UL_error)):
                        break
                    #print("BFUL", result.BF_UL)
                    if (math.isnan(result.BF_UL)):
                        break

                    result.optimal_window = 0
                    self.Results.append(result)
                    mom_high += self.momentum_Bin_width
                mom_low += self.momentum_Bin_width
            for i, j in enumerate(self.Results):
                print("=============================")
                print(i)
                j.PrintResults()

            # iterate over results_vector and find the optimal window with respect to the 90% Feldman-Cousins BF upper limit
            temp_index = -1
            temp_BF_UL = 999
            temp_SES_Opt = 999
            for i, j in enumerate(self.Results):
                if self.optimize_for == 'BFUL':
                    if (self.Results[i].BF_UL < temp_BF_UL and self.Results[i].BF_UL!=0):
                        temp_index = i
                        temp_BF_UL = self.Results[i].BF_UL
                if self.optimize_for == 'SES':

                    if (self.Results[i].SES < temp_SES_Opt and self.Results[i].SES!=0):
                        temp_index = i
                        temp_SES_Opt = self.Results[i].SES
            self.Results[temp_index].optimal_window=1 # set flag to 1 for the entry with the optimal window
            print("Optimal")
            self.Results[temp_index].PrintResults()

        def WriteHistograms(self):
            """function to make TTree"""
            c_dio=TCanvas()
            c_dio.Divide(2,2)
            c_dio.cd(1)
            self.Histos.histo_DIO_generated_reweighted.Draw('HIST')
            c_dio.cd(2)
            self.Histos.histo_DIO_reconstructed_reweighted.Scale(1/self.GetDIOSimEff())
            self.Histos.histo_DIO_reconstructed_reweighted.Draw('HIST')
            c_dio.SaveAs("DIO."+str(self.constants.target)+".root")

            c_signal=TCanvas()
            c_signal.Divide(2,2)
            c_signal.cd(1)
            self.Histos.histo_CE_generated.Draw('HIST')
            c_signal.cd(2)
            self.Histos.histo_CE_reconstructed.Scale(1/self.GetCESimEff())
            self.Histos.histo_CE_reconstructed.Draw('HIST')
            c_signal.SaveAs("CE."+str(self.constants.target)+".root")

            c_r=TCanvas()
            c_r.cd(1)
            ratio = TH1F("ratio", "ratio",400,90,110)
            for i in range(1,self.Histos.histo_DIO_reconstructed_reweighted.GetNbinsX()-1 ):
                d = self.Histos.histo_DIO_generated_reweighted.GetBinContent(i)
                n = self.Histos.histo_DIO_reconstructed_reweighted.GetBinContent(i)
                if(d!=0):
                    ir = (n/self.GetDIOSimEff())/d
                    ratio.Fill(ir)
            ratio.Draw('HIST')
            c_r.SaveAs("ratio"+str(self.constants.target)+".root")
