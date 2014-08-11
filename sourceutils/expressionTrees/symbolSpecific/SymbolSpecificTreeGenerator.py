
from sourceutils.tracking.TrackingInfoProvider import TrackingInfoProvider
from sourceutils.expressionTrees.treeCreation.ExpressionTreeProvider import ExpressionTreeProvider
from sourceutils.expressionTrees.symbolSpecific.SymbolPropagator import SymbolPropagator
from sourceutils.expressionTrees.symbolSpecific.ExpressionTreePruner import ExpressionTreePruner

class SymbolSpecificTree:
    def __init__(self):
        pass
    
    def setSymbol(self, symbol, symbolType):
        self.symbol = symbol
        self.symbolType = symbolType
    
    def setTrackingInfo(self, trackingInfo):
        self.trackingInfo = trackingInfo
    
    def setPrunedTree(self, prunedTree, nodesKept):
        self.prunedTree = prunedTree
        self.nodesKept = nodesKept

    def setSymbols(self, symbols):
        self.symbols = symbols

    # this is just for debugging/illustrations for paper
    def plot(self):
        import cPickle as pickle
        from sourceutils.plotting.ASTPlotter import ASTPlotter
        
        f = file('.tmp.pickl', 'w')
        pickle.dump(self.prunedTree, f)
        f.close()
        
        processor = ASTPlotter()
        processor.process('.tmp.pickl')

class SymbolSpecificTreeGenerator:
    def __init__(self):

        self.expressionTreeProvider = ExpressionTreeProvider()
        self.trackingInfoProvider = TrackingInfoProvider()
        self.symbolPropagator = SymbolPropagator()
        self.exprTreePruner = ExpressionTreePruner()

    def getTree(self, location, symbol):
        
        self.location = location

        trackingInfo = self.trackingInfoProvider.loadTrackingInfo(location)
        tree = self.expressionTreeProvider.loadExpressionTree(location)
        
        self.newTree = SymbolSpecificTree()
        self.newTree.setTrackingInfo(trackingInfo)
        
        (symbol, symbolType) = self._parseSymbol(symbol)
        self.newTree.setSymbol(symbol, symbolType)
        self._setAssociatedSymbols()
        self._setExpressionTreeForSymbols(tree)
        
        return self.newTree
    
    def _parseSymbol(self,s):
        s = s[2:-2]
        
        if s.startswith('type: '):
            return (s[len('type: '):], 'type')
        
        if s.startswith('call: '):
            self.isCall = True
            return (s[len('call: '):], 'call')
        
        elif s.startswith('param: '):
            return (s.split(' ')[-1], 'param')
        elif s.startswith('local: '): 
            return (s.split(' ')[-1], 'local')
        
        return (s, 'stray')
    
    def _setAssociatedSymbols(self):
        trackingInfo = self.newTree.trackingInfo
        symbol = self.newTree.symbol
        symbolType = self.newTree.symbolType
        symbols = self.symbolPropagator.propagate(trackingInfo, symbol, symbolType)
        # print 'FOO %s %s: %s' % (symbol, self.location, symbols)
        self.newTree.setSymbols(symbols)
    
    def _setExpressionTreeForSymbols(self, tree):
        # exprTree = copy.deepcopy(tree.prunedTree)
        exprTree = tree.prunedTree
        (prunedTree, nodesKept) = self.exprTreePruner.pruneForSymbols(exprTree, self.newTree.symbols)
        self.newTree.setPrunedTree(prunedTree, nodesKept)
        