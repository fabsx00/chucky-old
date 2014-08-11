
from libjoern.pythonast.PythonASTProcessor import PythonASTProcessor
from DotDrawer import DotDrawer

class ASTPlotter(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
        self.drawer = DotDrawer()

    def process(self, treeFilename):
        self.loadTreeFromFile(treeFilename)
        self.handlePrunedTree()

    def handlePrunedTree(self):
        
        prunedTree = self.tree.parent
        
        self.drawer.beginDraw()
        self.drawer.drawHeader()
        self._traverseFunction(prunedTree)
        self.drawer.drawFooter()
        self.drawer.endDraw()
    
    def _traverseFunction(self, node):
        
        if len(node.row) > 0 and node.row[0] == 'LEAF_NODE': return -1
        
        
        # if len(node.children) >0 and len(node.row) > 2:
        #     node.row = node.row[:1]
        if len(node.row) > 2:
            node.row = [node.row[0], node.row[4]]
        

        rootNodeLabel = str(node.row)
        # if rootNodeLabel.find('[\'water') == 0:
        #    style = 'dashed'
        #    fontColor = 'grey'
        # else:
        style=''
        fontColor = 'black'
            
        rootNodeId = self.drawer.drawNode(rootNodeLabel, 'http://foo', 'white', style, fontColor)
        for child in node.children:
            childNodeId = self._traverseFunction(child)
            if childNodeId == -1: continue
            self.drawer.drawLink(rootNodeId, childNodeId)
        
        return rootNodeId
        