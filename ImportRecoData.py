# Author : S Middleton
# Date : 2020
# Purpose : Prototype Importer Class

import sys
import uproot
import pandas
import math

class ImportRecoData :

    def __init__(self, CEfileName, DIOfileName , RPCextfileName, RPCintfileName, CosmicsfileName=False, treeName = "TrkAnaNeg", branchName = "trkana"):
        """ Initialise the Class Object """
        self.CEFileName= CEfileName
        self.DIOFileName= DIOfileName
        self.RPCextFileName= RPCintfileName
        self.RPCintFileName= RPCextfileName
        self.CosmicsFileName = CosmicsfileName
        self.TreeName = treeName
        self.BranchName = branchName

    def Import(self, process, flatten = False):
        """ Import root tree and save it as a pandas dataframe """
        df = []
        if process == "signal":
            input_file = uproot.open(self.CEFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)
        if process == "DIO":
            input_file = uproot.open(self.DIOFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)
        if process == "RPCext":
            input_file = uproot.open(self.RPCextFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)
        if process == "RPCint":
            input_file = uproot.open(self.RPCintFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)
        if process == "Cosmics":
            input_file = uproot.open(self.CosmicsFileName)
            input_tree = input_file[self.TreeName][self.BranchName]
            df = input_tree.pandas.df(flatten=flatten)
        return df

    def GetFeature(self, process, feature, flatten=False ):
        """ Open Root File and Extract Specified field """
        filename = ""
        if process == "CE":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName
        if process == "RPCext":
            filename = self.RPCextFileName
        if process == "RPCint":
            filename = self.RPCintFileName
        if process == "Cosmics":
            filename = self.CosmicsFileName
        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=flatten)
        return df[feature]

    def GetMagFeature(self, process, feature_x, feature_y, feature_z, flatten=False ):
        """ Open Root File and Extract field and find a magnitude """
        filename = ""
        if process == "CE":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName
        if process == "RPCext":
            filename = self.RPCextFileName
        if process == "RPCint":
            filename = self.RPCintFileName
        if process == "Cosmics":
            filename = self.CosmicsFileName
        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=flatten)
        df_tot = []
        for i, j in enumerate(df[feature_x]):
            fx = j
            fy = df[feature_y][i]
            fz = df[feature_z][i]
            df_tot.append(math.sqrt(fx*fx+fy*fy+fz*fz))
        return df_tot

    #TODO: Devloping this:
    def ExportDataToCSV(self, filename, flatten = False):
        """At some point we may want to use a CSV"""
        file = uproot.open(filename) #TODO
        electrons = file[self.TreeName][self.BranchName]
        df = electrons.pandas.df(flatten = flatten)
        df.to_csv("df.csv", index = False)
