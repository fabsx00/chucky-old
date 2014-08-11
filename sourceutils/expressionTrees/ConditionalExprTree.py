from sourceutils.expressionTrees.treeCreation.ASTToConditionalExprTree import ASTToConditionalExprTree

class ConditionalExprTree:
    def __init__(self):
        self.prunedTree = None
        self.nodesKept = []
         
    def initFromAST(self, ast):
        converter = ASTToConditionalExprTree()
        (self.prunedTree, self.nodesKept) = converter.pruneTree(ast)
        
    