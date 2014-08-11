
import cPickle as pickle

class SinkSnippetExtractor:


    def getSinkAreaSubtree(self, projectRoot, callToSink):
        subtree = self._getSinkNode(projectRoot, callToSink)            
        areaSubtree = self._getSubtreeForArea(subtree)
        return areaSubtree


    def _getSinkNode(self, projectRoot, (callRow, functionDir)):
        functionPicklFilename = '%s%s/func_ast.pickl' % (projectRoot, functionDir)
        f = file(functionPicklFilename)
        funcPickl = pickle.load(f)
        f.close()
        return funcPickl.searchNodeByRow(callRow)

    def _getSubtreeForArea(self, subtree):
        # Area: walk up to next stmts-node
        
        while not ((subtree.parent == None) or (subtree.row[0] == 'stmts')):
            subtree = subtree.parent
        return subtree
        