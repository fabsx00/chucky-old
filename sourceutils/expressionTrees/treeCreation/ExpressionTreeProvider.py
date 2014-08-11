
import os
import cPickle as pickle
from sourceutils.expressionTrees.treeCreation.ConditionalExprTreeGenerator import ConditionalExprTreeGenerator

class ExpressionTreeProvider:
    
    def __init__(self):
        self.exprTreeGenerator = ConditionalExprTreeGenerator()
        self.exprTrees = {}
    
    def loadExpressionTree(self, location):
        filename = location + '/expr_tree.pickl'
        
        if filename in self.exprTrees:
            return self.exprTrees[filename]

        if not os.path.exists(filename):
            exprTree = self.exprTreeGenerator.generateTreeForLocation(location)
            self.exprTreeGenerator.saveTreeForLocation(exprTree, location)
        else:
            exprTree = pickle.load(file(filename))
        
        self.exprTrees[filename] = exprTree
        return self.exprTrees[filename]
        