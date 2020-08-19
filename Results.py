# Author : S Middleton
# Date : 2020
# Purpose : Will store Results of the calculations

# TODO - this class should be slight into the different purposed structs


class Results :

    def __init__(self):
        self.momentum_low = 0
        self.momentum_high = 0

        #Yields :
        self.N_CE_gen = 0
        self.N_CE_rec = 0
        self.N_CE_expected = 0
        self.N_CE_expected_error = 0

        self.N_DIO_gen = 0
        self.N_DIO_gen_error = 0
        self.N_DIO_rec = 0
        self.N_DIO_rec_error = 0
        self.N_DIO_expected = 0
        self.N_DIO_expected_error = 0

        self.N_intRPC_gen = 0
        self.N_intRPC_rec = 0
        self.N_intRPCs_expected = 0
        self.N_intRPCs_expected_error = 0

        self.N_extRPC_gen = 0
        self.N_extRPC_rec = 0
        self.N_extRPCs_expected = 0
        self.N_extRPCs_expected_error = 0

        # Efficiencies:

        self.efficiency_DIO = 0
        self.efficiency_error_DIO = 0

        self.efficiency_intRPC = 0
        self.efficiency_error_intRPC = 0

        self.efficiency_extRPC = 0
        self.efficiency_error_extRPC = 0

        self.efficiency_CE = 0
        self.efficiency_error_CE = 0

        # StatsResults:
        self.Nsig_UL = 0
        self.Nsig_UL_error = 0
        self.BF_UL = 0
        self.BF_UL_error = 0
        self.SES = 0
        self.SES_error = 0
        self.optimal_window = 0

    def PrintResults(self):
        """ prints the results to screen """
        print("Mom Window Start",self.momentum_low)
        print("Mom Window End", self.momentum_high)
        print("NCE Gen", self.N_CE_gen)
        print("NCE Reco", self.N_CE_rec)
        print("CE Eff", self.efficiency_CE,  "+/-", self.efficiency_error_CE)
        print("CE Expected", self.N_CE_expected, "+/-", self.N_CE_expected_error)

        print("NDIO Gen", self.N_DIO_gen,  "+/-", self.N_DIO_gen_error)
        print("NDIO Reco",self.N_DIO_rec, "+/-", self.N_DIO_rec_error)
        print("NDIO Expected", self.N_DIO_expected, "+/-", self.N_DIO_expected_error)
        print("DIO Eff", self.efficiency_DIO,  "+/-", self.efficiency_error_DIO)

        print("N Internal RPC Gen", self.N_intRPC_gen,  "+/-" )
        print("N Internal RPC Reco",self.N_intRPC_rec, "+/-")
        print("Intenral Conversions Expected", self.N_intRPCs_expected, "+/-",  self.N_intRPCs_expected_error)
        print("Internal RPC Eff", self.efficiency_intRPC,  "+/-", self.efficiency_error_intRPC)

        print("N External RPC Gen", self.N_extRPC_gen,  "+/-")
        print("N External RPC Reco",self.N_extRPC_rec, "+/-")
        print("External RPC Expected", self.N_extRPCs_expected, "+/-",  self.N_extRPCs_expected_error)
        print("External RPC Eff", self.efficiency_extRPC,  "+/-", self.efficiency_error_extRPC)

        print("SES", self.SES, "+/-",self.SES_error)
        print("Sig UL",self.Nsig_UL, "+/-", self.Nsig_UL_error)
        print("BFUL", self.BF_UL, "+/-", self.BF_UL_error )
