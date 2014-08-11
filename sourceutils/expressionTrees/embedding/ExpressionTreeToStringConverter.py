
from libjoern.pythonast.TreeToStringsConverter import TreeToStringsConverter

class ExpressionTreeToStringsConverter(TreeToStringsConverter):
    def __init__(self):
        TreeToStringsConverter.__init__(self)
    
    def leafNodeToString(self, node):
        return '@+%s+@' % (str(node.row[1]))
    
    def nonLeafNodeToString(self, node, immediateChildStrings):
        return '@+%s%s+@' % (str(node.row[0]), ''.join(immediateChildStrings))
    
    def includeLeafNode(self, node):
        if node.getType() in ['REL_OPERATOR', 'EQ_OPERATOR', 'ASSIGN_OP']:
            return False
        elif node.row[1] == '$NUM':
            return False
        elif node.row[1] == 'NULL':
            return False
        return True
    
    def skipChildExpansion(self, child):
        # discards arguments of calls!
        # might want to remove this but need tracking then
        if child.getType() == 'ARGUMENT':
            return True
        return False
