import re

from sourceutils.expressionTrees.embedding.ExpressionTreeNormalizer import ExpressionTreeNormalizer
from sourceutils.expressionTrees.embedding.ExpressionTreeToStringConverter import ExpressionTreeToStringsConverter
from sourceutils.expressionTrees.symbolSpecific.SymbolSpecificTreeProvider import SymbolSpecificTreeProvider

class TreeToExpressionConverter:
    def __init__(self):
        self.symbolTreeProvider = SymbolSpecificTreeProvider()
        
        self.exprTreeNormalizer = ExpressionTreeNormalizer()
        self.treeToStrings = ExpressionTreeToStringsConverter()
    
    def getExpressionsForSymbol(self, location, symbolOfInterest):
        
        treeForSymbol = self.symbolTreeProvider.getTree(location, symbolOfInterest)
        expressions = self._normalizeTree(treeForSymbol)
        return expressions
    
    def _normalizeTree(self, treeForSymbol):
        self.exprTreeNormalizer.normalize(treeForSymbol)
        expressions = self.expressionsFromTree(treeForSymbol.prunedTree, treeForSymbol.nodesKept)
        return expressions
    
    def expressionsFromTree(self, tree, nodesKept):
        expressions = []
        for node in nodesKept:
            
            # skip COND-nodes and go down to EXPR-nodes
            for c in node.children:
                newExpressions = self.treeToStrings.allSubtreesAsString(c)
                expressions.extend(newExpressions)
                
        return expressions
    
    
    