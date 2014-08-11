from sourceutils.misc.GzipPickler import GzipPickler

from libjoern.pythonast.PythonASTTreeNode import PythonASTTreeNode #@UnusedImport
             
class PythonASTProcessor():
    """
    Implements depth-first traversal on ASTs.
    defaultHandler is called before entering
    children (pre-order).
    """
    def __init__(self):
        
        self.handlers = dict()
        self.currentFile = None
    
    def defaultHandler(self, node):
        return False
    
    def loadTreeFromFile(self, treefilename):

        self.currentFile = self._treefileToSourceFile(treefilename)

        p = GzipPickler()
        
        try:
            self.tree = p.load(treefilename).prunedTree.children[0]
        except:
            self.tree = p.load(treefilename).children[0]
    
    def _treefileToSourceFile(self, treefile):
        return ('/'.join(treefile.split('/')[:-1]))
    
    def processTree(self, node):

        if node == None:
            node = self.tree
            
        traverseChildren = self._callHandlers(node)
        if traverseChildren:
            self.processChildren(node)

    def processChildren(self, node = None):
        if node == None:
            node = self.tree
        
        for child in node.children:
            self.processTree(child)

    def _callHandlers(self, node):
        nodeType = node.row[0]
        if nodeType in self.handlers:
            handler = self.handlers[nodeType]
            return handler(node)
        return self.defaultHandler(node)
    
    