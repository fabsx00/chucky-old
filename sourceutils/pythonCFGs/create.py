#!/usr/bin/env python2
from CSVToCFG import CSV2CFG
from libjoern.FileIterators import SourceFileASTIterator

def extractCSVCFGs(projectRoot):

    codeTreeWalker = SourceFileASTIterator(projectRoot)
       
    for metaDataFile in codeTreeWalker:
        print metaDataFile
        processor = CSV2CFG()
        processor.processCSVRows(metaDataFile)
        processor.terminateFunction()
    
def main(projectRoot):
    print("Creating PythonCFGs for " + projectRoot)
    extractCSVCFGs(projectRoot)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])