from libjoern.pythonast.TreePruner import TreePruner
from libjoern.ASTNodeTypes import CONDITION, LEAF_NODE, DESTINATION

"""
TODO: An API should be used to access nodes of the AST.
"""

class ASTToConditionalExprTree(TreePruner):
    
    def __init__(self):
        TreePruner.__init__(self)
    
    def keepNode(self, node):
        nodeType = node.getType()
        if nodeType == CONDITION:
            return True
        
        if nodeType == DESTINATION:
            if node.parent.children[0].row[4] == 'return':
                return True
        
        # if nodeType == 'FUNCTION_CALL':
        #    return True
        
        return False
    
    def postProcess(self):
        self.nodesDiscovered = []
        for c in self.nodesKept:
            self.cleanupConditionalNode(c)
        self.nodesKept.extend(self.nodesDiscovered)
        
    def cleanupConditionalNode(self, node):
        
        nodeType = node.getType()
        
        # remove leafs from conditional nodes
        if nodeType == LEAF_NODE:
            return None
        
        # This prunes children of unary expressions
        # if nodeType in ['FIELD', 'UNARY_OPERATOR'] and node.parent.getType() == 'UNARY_EXPR':
        #    return None
        
        if nodeType == 'UNARY_OPERATOR' and node.parent.getType() == 'UNARY_EXPR':
            return None
        
        if nodeType == 'FIELD' and node.parent.getType() == 'UNARY_EXPR':
            # print 'FOO: %s' % (node.row)
            parent = node.parent
            if parent.children[0].row[4] in ['*', '!']:
                if len(parent.children) > 1:
                    if parent.children[1].row[4] != '(':
                        return None
                else:
                    return None


        if nodeType == CONDITION and node not in self.nodesKept:
            self.nodesDiscovered.append(node)
                
        # remove argument lists
        # if nodeType == 'ARGUMENT_LIST':
        #    return None
        
        newChildren = self.cleanupCondNodeChildren(node)
        node.children = newChildren
        
        
        node.row = self._keepOnlyNodeTypeAndSymbol(node.row)
        
        return node

    def cleanupCondNodeChildren(self, node):
        newChildren = [self.cleanupConditionalNode(c) for c in node.children]
        newChildren = [c for c in newChildren if c]
        return newChildren
    
    def _keepOnlyNodeTypeAndSymbol(self, row):
        
        symbol = row[4]
        return [row[0], symbol]
    
    def _keepOnlyNodeType(self, row):
        return [row[0], ""]
