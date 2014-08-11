import os
import cPickle as pickle
from sourceutils.misc.GzipPickler import GzipPickler

from libjoern.pythonast.SubtreeProcessors import getFunctionNameForFunction
from libjoern.pythonast.PythonASTIterators import FunctionASTIterator

class FunctionASTExtractor(FunctionASTIterator):
    def __init__(self):
        FunctionASTIterator.__init__(self)
            
    def handler(self, node):
        self.dumpTree(node)
        return False
            
    def dumpTree(self, node):
        
        csvRow = self.functionRow
        functionName = getFunctionNameForFunction(node)
        pos = csvRow[1]
        
        outputDir = self.currentFile
        outputDir += '/' + functionName + '_' + pos.replace(':', '_')
        
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        
        outputFilename = outputDir + '/func_ast.csv'
        f = file(outputFilename, 'w')
        f.write(node.toCSV())
        f.close()
        
        parent = node.parent
        node.parent = None
        outputFilename = outputDir + '/func_ast.pickl'
        GzipPickler().dump(node, outputFilename)
        node.parent = parent
    