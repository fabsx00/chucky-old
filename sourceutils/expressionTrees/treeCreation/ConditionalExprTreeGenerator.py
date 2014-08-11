import cPickle as pickle
from sourceutils.misc.GzipPickler import GzipPickler

from sourceutils.expressionTrees.ConditionalExprTree import ConditionalExprTree

class ConditionalExprTreeGenerator:
    def __init__(self):
        pass
    
    def generateTreeForLocation(self, location):
        exprTree = ConditionalExprTree()
        originalAST = self._getASTForLocation(location)
        exprTree.initFromAST(originalAST)
        return exprTree

    def saveTreeForLocation(self, exprTree, location):
        outputFilename = location + '/expr_tree.pickl'
        pickle.dump(exprTree, file(outputFilename, 'w'), protocol=2)

    def _getASTForLocation(self, location):
        return GzipPickler().load(location + '/func_ast.pickl')
        # return pickle.load(file(location + '/func_ast.pickl'))
    

