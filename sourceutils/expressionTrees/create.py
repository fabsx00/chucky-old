#!/usr/bin/env python2

from libjoern.FileIterators import FunctionPythonASTIterator
from sourceutils.expressionTrees.treeCreation.ConditionalExprTreeGenerator import ConditionalExprTreeGenerator

import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))

def outFilenameFromCSVFilename(csvFilename):
    outputFilename = '/'.join(csvFilename.split('/')[:-1])
    outputFilename += '/' + 'ast.pickl'
    return outputFilename
        
def main(projectRoot):
   
    print('Creating Conditional Expression Trees for %s' %(projectRoot))
    
    codeTreeWalker = FunctionPythonASTIterator(projectRoot)
    
    for picklFilename in codeTreeWalker:
        location = picklFilename[:-(len('func_ast.pickl'))]
        print location
        processor = ConditionalExprTreeGenerator()
        processor.createTreeForLocation(location)
            
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    