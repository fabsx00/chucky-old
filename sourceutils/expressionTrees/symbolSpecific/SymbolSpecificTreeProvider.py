
import base64
import os

from sourceutils.expressionTrees.symbolSpecific.SymbolSpecificTreeGenerator import SymbolSpecificTreeGenerator
from sourceutils.misc.GzipPickler import GzipPickler

class SymbolSpecificTreeProvider:
    
    def __init__(self):

        self.treeGenerator = SymbolSpecificTreeGenerator()
        self.symbolTrees = {}
    
        self.writeToDisk = False

    def getTree(self, location, symbol):

        if self._treeIsCached(location, symbol):
            return self._getTreeFromCache(location, symbol)
        
        # Tree is not in cache.
        if self._treeIsOnDisk(location, symbol):
            treeForSymbol = self._loadTreeFromDisk(location, symbol)
        else:
            treeForSymbol = self.treeGenerator.getTree(location, symbol)
            if self.writeToDisk:
                self.writeTreeToDisk(treeForSymbol, location, symbol)
                
        # cache tree and return it.
        self.symbolTrees[(location, symbol)] = treeForSymbol
        return treeForSymbol
        
    def _treeIsCached(self, location, symbol):
        return (location, symbol) in self.symbolTrees

    def _getTreeFromCache(self, location, symbol):
        return self.symbolTrees[(location, symbol)]
    
    def _treeIsOnDisk(self, location, symbol):
        filename = self._getFilenameForTree(location, symbol)
        return os.path.exists(filename)

    def _loadTreeFromDisk(self, location, symbol):
        filename = self._getFilenameForTree(location, symbol)
        return GzipPickler().load(filename)
    
    def writeTreeToDisk(self, tree, location, symbol):
        filename = self._getFilenameForTree(location, symbol)
        dirName = '/'.join(filename.split('/')[:-1])
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        GzipPickler().dump(tree, filename)

    def _getDirectoryForTree(self, location, symbol):
        dirName = location + '/'
        dirName += base64.b64encode(symbol)
        return dirName

    def _getFilenameForTree(self, location, symbol):
        dirName = self._getDirectoryForTree(location, symbol)
        filename = dirName + '/' + 'expr_tree.pickl'
        return filename
        
    