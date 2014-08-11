#!/usr/bin/env python2


from sourceutils.functionASTs.FunctionASTExtractor import FunctionASTExtractor
from libjoern.FileIterators import SourceFilePythonASTIterator

import sys

def main(projectRoot):

    print 'Creating function-ASTs'
    codeTreeWalker = SourceFilePythonASTIterator(projectRoot)
    processor = FunctionASTExtractor()
           
    for pythonASTFilename in codeTreeWalker:
        processor.loadTreeFromFile(pythonASTFilename)
        processor.processChildren()
   
if __name__ == '__main__':
    main(sys.argv[1])