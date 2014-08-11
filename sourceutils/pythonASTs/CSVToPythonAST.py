import cPickle as pickle

from libjoern.csvast.CSVProcessor import CSVProcessor
from libjoern.csvast.CSVRowAccessors import getCSVRowLevel
from libjoern.pythonast.PythonASTTreeNode import PythonASTTreeNode

"""
This class implements conversion from
Abstract Syntax Trees in CSV format
to trees of PythonASTTreeNodes.
To do this, only the level-field of each
row needs to be accounted for.
"""

class CSVToPythonAST(CSVProcessor):
    def __init__(self):
        CSVProcessor.__init__(self)
        
        self.rootNode = PythonASTTreeNode(None)
        self.parentStack = []
        self.previousNode = self.rootNode
        
        self.defaultHandler = self.handleNode
    
    def handleNode(self, row):
        
        newNode = PythonASTTreeNode(row) 
        
        # code below fails if level ever
        # increases by more than one at once
        level = int(getCSVRowLevel(row))
        if level > len(self.parentStack) - 1:
            # moved down one level, push previous node
            self.parentStack.append(self.previousNode)
        elif level < len(self.parentStack) -1:
            while(level < len(self.parentStack) - 1):
                self.parentStack.pop()
        else:
            # stayed on a level, no need to adjust parentStack
            pass
                
        parentNode = self.parentStack[-1]
        parentNode.appendChild(newNode)
        newNode.parent = parentNode
        
        self.previousNode = newNode
    
    def prettyPrintTree(self):
        numberOfTabs = 0
        self._prettyPrintTree(self.rootNode, numberOfTabs)
    
    def _prettyPrintTree(self, node, numberOfTabs):
        outString = '\t'*numberOfTabs
        outString += str(node.row)
        print(outString)
        for child in node.children:
            self._prettyPrintTree(child, numberOfTabs + 1)
    
    def saveResults(self, filename):
        from sourceutils.misc.GzipPickler import GzipPickler
        p = GzipPickler()
        p.dump(self.rootNode, filename)
        


