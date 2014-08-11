from libjoern.pythonast.TreePrunerDuplicate import TreePrunerDuplicate
# from libjoern.pythonast.TreePruner import TreePruner as TreePrunerDuplicate
from libjoern.ASTNodeTypes import CONDITION, DESTINATION

import re

class ExpressionTreePruner(TreePrunerDuplicate):
    def __init__(self):
        TreePrunerDuplicate.__init__(self)
    
    def pruneForSymbols(self, ast, symbols):
        self.symbols = symbols
        (prunedTree, nodesKept) = self.pruneTree(ast)
        return (prunedTree, nodesKept)
        
    def keepNode(self, node):
        nodeType = node.getType()
        if not nodeType in [CONDITION,DESTINATION]:
            return False
        
        return self.subtreeRefersToSymbol(node)
        
    def subtreeRefersToSymbol(self, node):
        
        if node.children == []:
            return self.anySymbolOccursInNode(node)
        else:
            for child in node.children:
                keep = self.subtreeRefersToSymbol(child)
                if keep:
                    return True
            return False
    
    def postProcess(self):
        self.nodesDiscovered = []
        for c in self.nodesKept:
            self.findConditionsInCondition(c)
        self.nodesKept.extend(self.nodesDiscovered)

    def findConditionsInCondition(self, node):
        nodeType = node.getType()
        
        if nodeType == 'CONDITION' and node not in self.nodesKept:
            self.nodesDiscovered.append(node)
        
        for c in node.children:
            self.findConditionsInCondition(c)
        
    def anySymbolOccursInNode(self, node):
        # '(?<!\w)(%s)(?!(\w|(\s\.)|(\s->)))'
        for symbol in self.symbols:
            if re.search('(?<!\w)(%s)(?!(\w))' % (re.escape(symbol)), node.row[1]):
                return True
        return False
