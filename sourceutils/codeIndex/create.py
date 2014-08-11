#!/usr/bin/env python2

from libjoern.FileIterators import FunctionASTIterator

from CodeIndexCreator import CodeIndexCreator
import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))

def main(projectRoot):
   
    print('Creating index for %s' %(projectRoot))
    
    codeTreeWalker = FunctionASTIterator(projectRoot)
    processor = CodeIndexCreator(projectRoot)
   
    for csvFilename in codeTreeWalker:
        processor.processCSVRows(csvFilename)
    processor.saveResults()
    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    