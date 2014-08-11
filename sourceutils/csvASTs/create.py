#!/usr/bin/env python2

from CodeToCSVAST import CodeToCSVAST
from libjoern.FileIterators import  SourceFileWalker

import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))
        
def main(projectRoot):
   
    print('Creating ASTs in CSV format for %s' %(projectRoot))
    
    codeTreeWalker = SourceFileWalker(projectRoot)
    codeToCSVAST = CodeToCSVAST()
    
    for sourceFile in codeTreeWalker:
        print sourceFile
        dirForSourceFile = codeTreeWalker.getDirForFilename(sourceFile)
        codeToCSVAST.run(sourceFile, dirForSourceFile)
  
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    