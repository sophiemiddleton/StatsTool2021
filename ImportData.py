# Author : S Middleton
# Date : 2020
# Purpose : Prototype Importer Class

import sys
import uproot
import pandas

class ImportData :

    def __init__(self, fileName , treeName = TrkAnaNeg, branchName = trkana, flatten = False, featureList = None):
        """ Initialise the Class Object """
        self.FileName= fileName
        self.TreeName = treeName
        self.BranchName = branchName
        self.FeatureName = featureList
        self.Flatten = flatten

    def Import(self):
        """ Import root tree and save it as a pandas dataframe """
        input_file = uproot.open(self.FileName)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=self.Flatten)
        return df

    def GetFeature(self):
        """ Open Root File and Extract Specified field """
        Features = []
        input_file = uproot.open(self.FileName)
        input_tree = input_file[self.TreeName][self.BranchName]
        df = input_tree.pandas.df(flatten=self.Flatten)
        print(df[self.FeatureName].describe())
        print(df[self.FeatureName])
        return df[self.FeatureName]

    def ExportDataToCSV(self):
        """At some point we may want to use a CSV"""
        file = uproot.open(self.FileName)
        electrons = file[self.TreeName][self.BranchName]
        df = electrons.pandas.df(flatten = self.Flatten)
        df.to_csv("df.csv", index = False)
