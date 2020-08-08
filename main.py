# Author: S Middleton
# Date: 2020
# Purpose: Import Data to StatsTool

import sys
from ImportClass import ImportData
import StatsFunctions 

def main(file_name, tree_name, branch_name, feature_name):
    i = ImportData(file_name, tree_name, branch_name)

if __name__ == "__main__":
    print("Executing with ", sys.argv)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Finished")
