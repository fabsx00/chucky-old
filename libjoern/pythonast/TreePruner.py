from libjoern.pythonast.PythonASTTreeNode import PythonASTTreeNode

class TreePruner:
    """
    Base Class for pruning of ASTs.
    
    Override method "keepNode" to specify
    the properties a node must fulfill to
    be kept. When calling "pruneTree" all
    other nodes will be removed unless they
    lead to a node that needs to be kept, in
    which case only the node's type is kept.
    
    The pruning operation therefore maintains
    the structure of the tree.
    
    """
    
    def __init__(self):
        self._reset()
    
    def _reset(self):
        self.prunedTree = None
        self.nodesKept = []
    
    
    def keepNode(self, node):
        """
        Override this method to specify
        the properties a node must fulfill
        to be kept.
        """
        return True

    def postProcess(self):
        """
        Override this function to perform
        post-processing. Nodes kept are 
        accessible via self.nodesKept and
        the prunedTree can be accessed via
        self.prunedTree.
        """
        pass
        
    def pruneTree(self, ast):
        """
        Once "keepNode" and optionally
        "postProcess" has been overridden,
        call this method to prune the tree.
        
        Returns:
        prunedTree -- the pruned tree
        nodesKept -- a list of references to
        the nodes deliberately kept alive (as
        opposed to those nodes, which were only
        kept as to not harm the tree structure).
        """
        
        self._reset()
        self.prunedTree = PythonASTTreeNode([])
        self.prunedTree.children = self._pruneAndPurgeChildren(ast, self.prunedTree)
        self.postProcess()
        return (self.prunedTree, self.nodesKept)

    def _pruneAndPurgeChildren(self, node, parent):
        newChildren =  [self._pruneAndPurge(child) for child in node.children]        
        newChildren = [c for c in newChildren if c]
        for c in newChildren:
            c.parent = parent
        return newChildren
    
    def _pruneAndPurge(self, node):
        
        if self.keepNode(node):
            self.nodesKept.append(node)
            newNode = node
            return newNode
        
        # For all other subtrees, keep only type
        # and traverse children
        newNode = self._purge(node)
        newNode.children = self._pruneAndPurgeChildren(node, newNode)
        
        # This makes sure we discard subtrees not containing
        # anything of interest
        if newNode.hasNoChildren():
            return None
        
        return newNode
    
    def _purge(self, node):
        # this isn't nice because we assume that
        # type is saved at node.row[0].
        return PythonASTTreeNode([node.getType()])
    