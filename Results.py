# Author : S Middleton
# Date : 2020
# Purpose : Will store Results of the calculations

class Results :

    def __init__(self):
        self.momentum_low = 0
        self.momentum_high = 0

        self.efficiency_CE = 0
        self.efficiency_error_CE = 0

        self.N_CE_gen = 0
        self.N_CE_rec = 0
        self.N_CE_expected = 0
        self.N_CE_expected_error = 0

        self.N_DIO_gen = 0
        self.N_DIO_gen_error = 0
        self.N_DIO_rec = 0
        self.N_DIO_rec_error = 0

        self.efficiency_DIO = 0
        self.efficiency_error_DIO = 0

        self.N_DIO_expected = 0
        self.N_DIO_expected_error = 0

        self.efficiency_intRPC = 0
        self.efficiency_extRPC = 0

        self.N_intRPCs_expected = 0
        self.N_intRPCs_expected_error = 0
        self.N_extRPCs_expected = 0
        self.N_extRPCs_expected_error = 0

        self.Nsig_UL = 0
        self.Nsig_UL_error = 0
        self.BF_UL = 0
        self.BF_UL_error = 0
        self.SES = 0
        self.SES_error = 0
        self.optimal_window = 0

    def PrintResults(self):
        """ prints the results to screen """
        print("Mom Start",self.momentum_low)
        print("Mom End", self.momentum_high)
        print("NCE Gen", self.N_CE_gen)
        print("NCE Reco", self.N_CE_rec)
        print("CE Eff", self.efficiency_CE,  "+/-", self.efficiency_error_CE)
        print("CE Expected", self.N_CE_expected, "+/-", self.N_CE_expected_error)
        print("SES", self.SES, "+/-",self.SES_error)
        print("DIO Gen", self.N_DIO_gen,  "+/-", self.N_DIO_gen_error)
        print("DIO Reco",self.N_DIO_rec, "+/-", self.N_DIO_rec_error)
        print("DIO Eff", self.efficiency_DIO,  "+/-", self.efficiency_error_DIO)
        print("DIO Expected", self.N_DIO_expected, "+/-", self.N_DIO_expected_error)
        print("RPC Expected", self.N_intRPCs_expected, "+/-",  self.N_extRPCs_expected)
        print("Sig uL",self.Nsig_UL, "+/-", self.Nsig_UL_error)
        print("BFUL", self.BF_UL, "+/-", self.BF_UL_error )
