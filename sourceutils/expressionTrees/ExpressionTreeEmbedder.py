
from mlutils.termDocMatrix.NameDictMapToMatrix import NameDictMapToMatrix
from sourceutils.misc.OccurrenceCounter import OccurrenceCounter
from sourceutils.misc.NameToDictMap import NameToDictMap

from sourceutils.tracking.TrackingInfoProvider import TrackingInfoProvider
from sourceutils.expressionTrees.treeCreation.ExpressionTreeProvider import ExpressionTreeProvider
from sourceutils.expressionTrees.TreeToExpressionConverter import TreeToExpressionConverter


class ExpressionTreeEmbedder:
    def __init__(self):
    
        self.exprTreeProvider = ExpressionTreeProvider()
        self.trackingInfoProvider = TrackingInfoProvider()
        self.treeToExprConverter = TreeToExpressionConverter()
    
    def embed(self, context, symbol):
        return self._termDocumentMatrixFromContext(context, symbol)
    
    def _termDocumentMatrixFromContext(self, context, symbol):
        
        x = self._termDictsFromContext(context, symbol)
        if x == None: return None
        (vecs, allNgrams)= x
                
        self.nameDictMapToMatrix = NameDictMapToMatrix()
        self.nameDictMapToMatrix.convertFromDicts(vecs, allNgrams)
        termDocMatrix = self.nameDictMapToMatrix.termDocumentMatrix
        return termDocMatrix

    def _termDictsFromContext(self, context, symbol):
        
        vecs = NameToDictMap()
        allNgrams = OccurrenceCounter()
        
        context.neighbours.append(context.origin)
        
        for neighbour in context.neighbours:
            nOcc = neighbour.nOccurrences
            location = neighbour.location
            expressions = self.treeToExprConverter.getExpressionsForSymbol(location, symbol)
            # expressions.append('@+$_+@')
            # expressions.append('@+EXPR@+$_+@+@')
            
            # print 'FOO %s: %s: %s' % (symbol, location, expressions)
            
            neighbour.setExpressions(expressions)

            # add null-vector for function if it does not contain expressions
            if len(expressions) == 0:
                vecs.add(None, location)
            
            for expr in expressions:
                # vecs.add(expr, location, 1.0/nOcc)
                # vecs.add(expr, location, 1.0)
                vecs.setItem(expr, location, 1.0)
                allNgrams.add(expr)            
        
        context.neighbours.pop()
        
        if len(vecs.d) == 0 or len(allNgrams.d) == 0:
            return None
    
        return (vecs, allNgrams)
                   
    def getAllConditionNodes(self):
        return self.tree.conditionalNodes

    
    
        
        
    