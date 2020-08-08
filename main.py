#!/usr/bin/python
# Author: S Middleton
# Date: 2020
# Purpose: Import Data to StatsTool

import sys
import argparse
import ImportData
import StatsFunctions

def main(file_name, tree_name, branch_name, feature_name):
    i = ImportData(file_name) #TODO - how to deal with multiple files

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
    parser.add_option('-a','--CE', dest='CE', default = 'CEData.root',help='NTuple with CE', metavar='Cedir')
    parser.add_option('-o','--DIO', dest='DIO', default = 'DIOData.root',help='NTuple with DIO', metavar='Diodir')
    #TODO - add in RPC and Cosmics
    parser.add_option('--tag', dest='tag', default = '1',help='file tag', metavar='tag')

    (options, args) = parser.parse_args()

    main(options,args);

    print("Finished")
