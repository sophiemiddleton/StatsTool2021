# Author : S Middleton
# Date : 2021
# Purpose : Constants

class Constants:

        def __init__(self, target, experiment):

            self.livegate = 700
            self.target = target
            if experiment == 'mu2e':
              self.POT= 3.6e20
            if experiment == 'mu2e2':
              self.POT = 5e22

            if target == 'Al':
                self.muonstopsperPOT = 0.00153814
                self.sim_ce_eff = 0.77
                self.sim_dio_eff = 0.47
                self.signal_start = 103.85
                self.signal_end = 105.1
                self.fixed_window_lower = 103.85
                self.fixed_window_upper = 105.1
            if target == 'Ti':
                self.muonstopsperPOT = 0.000108 #34
                # self.muonstopsperPOT = 0.0000886 # 25
                # self.muonstopsperPOT = 0.0000667 #17
                self.sim_ce_eff = 0.68#34: 0.68 # 17:0.68 25:70
                self.sim_dio_eff = 0.68 #34:0.74 # 17:0.68 25:73
                self.capturesperStop = 0.85
                self.decaysperStop = 0.15
                self.signal_start = 103.25
                self.signal_end = 104.5
                self.fixed_window_lower = 103.25
                self.fixed_window_upper = 104.5
            if target == 'V':
                #self.muonstopsperPOT = 0.00224 # - 34
                #self.muonstopsperPOT = 0.00243 #- 37
                #self.muonstopsperPOT = 0.00209 # - 30
                self.sim_ce_eff = 0.42
                self.sim_dio_eff = 0.62
                self.capturesperStop = 0.87
                self.decaysperStop = 0.13
                self.signal_start = 103.0
                self.signal_end = 104.25
                self.fixed_window_lower = 103.0
                self.fixed_window_upper = 104.25

            print("===================Information:============================")
            print("Number of Protons on Target:", self.POT)
            print("Target Material:", target)
            print("Muon Stopping Rate:", self.muonstopsperPOT)
            print("Captures Per Stop:", self.capturesperStop)
            print("Decays Per Stop:", self.decaysperStop)
            print("Default Signal Window (mom):", self.fixed_window_lower,"to",self.fixed_window_upper)
            print("===========================================================")
