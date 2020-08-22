# StatsTool2021

This code was developed by S. Middleton, the initial concept was based on the CalTool framework developed by M. Rohrken. But significant changes have since been made.

The purpose of this code is for the optimization of the Mu2e-II Stopping Target. I intend to maintain it and it will be used for the main sensitivity study eventually.

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

# Software Prereq.

To begin using this analysis package it is recommended that you install a few pre-requsities.

Firstly install:
* python3
* ROOT
* pyroot
* Pandas

These are essentials.

This package can be used on Mac and all linux machines.

For Mac please install pip : https://pip.pypa.io/en/stable/installing/ It makes life a lot easier.

Then install:

 * uproot : https://github.com/scikit-hep/uproot
 * uproot-methods
On a Mac you can then simply:

```
pip install uproot
```

Another thing I find useful is to create a virtual environment for the project. On mac follow this: https://sourabhbajaj.com/mac-setup/Python/virtualenv.html . It allows you to activate and deactivate the entire environment. Eventually we aim to have a setup script inside this Repo, meaning that all this would be obsolete. For now if you do want to do this you can simple pull the "requirements.txt":

```
$ virtualenv <env_name>
$ source <env_name>/bin/activate
(<env_name>)$ pip install -r path/to/requirements.txt

```

This can be a bit dangerous as you may have missed dependencies, but it will get you some way towards replicating the developer environments.
