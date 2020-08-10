# Author : S Middleton
# Date : 2020
# Purpose : Prototype Importer Class

import sys
import uproot
import pandas

class ImportData :

    def __init__(self, CEfileName, DIOfileName , treeName = "TrkAnaNeg", branchName = "trkana"):
        """ Initialise the Class Object """
        self.CEFileName= CEfileName
        self.DIOFileName= DIOfileName
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
        return df

    def GetFeature(self, process, feature, flatten=False ):
        """ Open Root File and Extract Specified field """
        filename = ""
        if process == "CE":
            filename = self.CEFileName
        if process == "DIO":
            filename = self.DIOFileName
        input_file = uproot.open(filename)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=flatten)
        return df[feature]

    #TODO: Devloping this:
    def ExportDataToCSV(self, filename, flatten = False):
        """At some point we may want to use a CSV"""
        file = uproot.open(filename) #TODO
        electrons = file[self.TreeName][self.BranchName]
        df = electrons.pandas.df(flatten = flatten)
        df.to_csv("df.csv", index = False)
