# StatsTool2021

This code was developed by S. Middleton, based on the CalTool framework developed by M. Rohrken.

The purpose of this code is for the optimization of the Mu2e-II Stopping Target.

# How to use

To use this code you must have made NTuple's using the Mu2e-II Offline Software.

The code takes in the Mu2e signal and 3 background NTuples:

* CE (signal)
* DIO
* RPCs
* Cosmics

Each NTuple must have the reconstructed Momentum and the generated Momentum.

A standard Mu2e-II analyzer can be use to generated ready-formatted NTuples for this study.

It is currently in development.

# To Run:

To run the code:

```python main.py --CE ... --DIO ... --RPC ... --Cosmics```

where you should replaced the ```...``` with the appropriate ROOT file.

# Prerequisites:

* python3
* UpRoot
* pandas
* pyROOT

Please see the ```requirements.txt```
