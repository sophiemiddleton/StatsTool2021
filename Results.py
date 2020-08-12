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
        print(" p_low  p_high  Ngen_CE  Nrec_CE             eff_CE        Nexp_CE                    SES               Ngen_DIO               Nrec_DIO            eff_DIO         Nexp_DIO         Nexp_RPC         NNsig_UL                  BF_UL\n");
        print("====================================================================================================================================================================================================================================\n");
        print(self.momentum_low,self.momentum_high,self.N_CE_gen,self.N_CE_rec,
        self.efficiency_CE,self.efficiency_error_CE,self.N_CE_expected,self.N_CE_expected_error,
        self.SES,self.SES_error,self.N_DIO_gen,self.N_DIO_gen_error,self.N_DIO_rec,self.N_DIO_rec_error,
        self.efficiency_DIO,self.efficiency_error_DIO,self.N_DIO_expected,self.N_DIO_expected_error,
        self.N_RPCs_expected,self.N_RPCs_expected_error,self.Nsig_UL,self.Nsig_UL_error,
        self.BF_UL,self.BF_UL_error )
