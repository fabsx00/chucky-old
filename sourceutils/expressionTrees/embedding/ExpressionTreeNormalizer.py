
import re
from libjoern.pythonast.PythonASTIterators import LeafIterator
from libjoern.ASTNodeTypes import REL_OPERATOR, EQ_OPERATOR, UNARY_OPERATOR
from libjoern.ASTNodeTypes import FIELD, CALLEE

class ExpressionTreeNormalizer(LeafIterator):

    def __init__(self):
        LeafIterator.__init__(self)
        self.handlers['EXPR'] = self.exprHandler
        self.handlers['UNARY_EXPR'] = self.unaryExprHandler

    def exprHandler(self, node):
        
        # if len(node.children) >= 3:
        #    for i in xrange(len(node.children) - 1):
        #        if not node.children[i].row[1] in ['==', '!=']:
        #            continue
        #        if node.children[i+1].row[1] in ['NULL', '0']:
        #            del node.children[i+1]
        #            del node.children[i]
        #            break
                
        return self.defaultHandler(node)
    
    def unaryExprHandler(self, node):
        
        
        if node.row[1].startswith('! '):
            if len(node.children) > 0:
                node.parent.children = node.children[:]
                # node.parent.children = [node.children[0]]
            else:
                node.row[0] = 'FIELD'
                node.row[1] = node.row[1][2:]
        
        return self.defaultHandler(node)


    def leafHandler(self, node):
        self.normalizeOperators(node)
        self.normalizeConstants(node)
        
        if self.symbolType == 'call':
            self.normalizeArgsAndRetvals(node)
        # else:
        #    self.normalizeTrackedVariables(node)
        # self.normalizeLocals(node)
        

    def normalizeLocals(self, node):
        nodeType = node.getType()
        if not nodeType in ['FIELD', 'UNARY_EXPR']:
            return

        if nodeType == 'FIELD':
            if node.row[1] in self.trackingInfo.locals:
                node.row[1] = '$_'
                # node.row[1] = self.trackingInfo.identifierToType[node.row[1]]
        elif nodeType == 'UNARY_EXPR':
            # this is dirty
            s = ' '.join(node.row[1].split(' ')[1:]) 
            if s in self.trackingInfo.locals:
                node.row[1].replace(s, '$_')

    def normalizeOperators(self, node):
        nodeType = node.getType()
        
        if not nodeType in [REL_OPERATOR, EQ_OPERATOR, UNARY_OPERATOR]:
            return
        
        if nodeType in [REL_OPERATOR, EQ_OPERATOR]:
            node.row[1] = '$CMP'
        elif nodeType == UNARY_OPERATOR:
            if node.row[1] == '!': node.row[1] = ''
    
    def normalizeConstants(self, node):
        nodeType = node.getType()
        if nodeType != FIELD:
            return
        
        if node.row[1].startswith('0x'):
            node.row[1] = node.row[1][2:]
        try:
            float(node.row[1])
            node.row[1] = '$NUM'
        except:
            pass
                
    def normalizeTrackedVariables(self, node):
        nodeType = node.getType()
        if node.row[1] == self.symbolOfInterest:
            node.row[1] = '$VAR'
        elif nodeType in ['FIELD', 'UNARY_EXPR']:
            
            # Note: We are deliberately only propagating by one hop here.
            # otherwise many things will seem checked, which are actually not
            if not self.trackingInfo.rvalToLval.has_key(self.symbolOfInterest):
                return            
            
            if node.row[1] in self.trackingInfo.rvalToLval[self.symbolOfInterest]:
                node.row[1] = '$VAR'
            
            if not self.trackingInfo.lvalToRval.has_key(self.symbolOfInterest):
                return            
            if node.row[1] in self.trackingInfo.lvalToRval[self.symbolOfInterest]:
                node.row[1] = '$VAR'
    
    def normalizeArgsAndRetvals(self, node):
        
        nodeType = node.getType()
        if node.row[1] == self.symbolOfInterest:
            if node.parent and node.parent.row[0] == 'FUNCTION_CALL':
                node.parent.children = []
                # node.parent.row[0] = 'FIELD'
                node.parent.row[1] = '$RET'
            # node.row[1] = '$RET'
        elif nodeType in ['FIELD', 'UNARY_EXPR']:
            
            # Note: We are deliberately only propagating by one hop here.
            # otherwise many things will seem checked, which are actually not
            if not self.trackingInfo.rvalToLval.has_key(self.symbolOfInterest):
                return
            if node.row[1] in self.trackingInfo.rvalToLval[self.symbolOfInterest]:
                node.row[1] = '$RET'
            
            if self.symbolOfInterest in self.trackingInfo.functionArguments:
                if node.row[1] in self.trackingInfo.functionArguments[self.symbolOfInterest]:
                    node.row[1] = '$ARG'
            
                # For arguments, propagate rvals once
                # if not self.trackingInfo.lvalToRval.has_key(node.row[1]):
                #    return            
                # if node.row[1] in self.trackingInfo.lvalToRval[node.row[1]]:
                #    node.row[1] = '$ARG'

    
    def normalize(self, treeForSymbol):
        
        self.symbolOfInterest = treeForSymbol.symbol
        self.symbolType = treeForSymbol.symbolType
        self.symbols = treeForSymbol.symbols
        self.trackingInfo = treeForSymbol.trackingInfo
        nodesKept = treeForSymbol.nodesKept
        
        for exprNode in nodesKept:
            self.processTree(exprNode)
        
    
    def getSymbolsInCondition(self, condNode):
                
        retList = []
        
        if self.isSymbol(condNode):
            retList = [condNode.row[1]]
        
        for c in condNode.children:
            retList.extend(self.getSymbolsInCondition(c))
        
        return retList
    
    def isSymbol(self, condNode):
        
        nodeType = condNode.row[0]
        condStr = condNode.row[1]

        if nodeType != 'UNARY_EXPR':
            return False
        
        if len(condStr) < 1:
            return False
        if condStr[0] == '(' or condStr == 'NULL':
            return False
        
        if condNode.children[0].row[0] == 'FUNCTION_CALL':
            return False
       
        return True
    
    def uniq(self, seq, idfun=None): 
        # order preserving
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result
    
    def replaceRvals(self, expressions, symOfInterest):
        newExpressions = []
        for e in expressions:
            newExpressions.extend(self._replaceRvals(e, symOfInterest))
        return newExpressions
    
    def _replaceRvals(self, expr, symOfInterest):
                
        # determine all rvalues containing the symbol
        # for each of these rvals, determine the lvals
        # replace lval in expr
        
        for rval in self.trackingInfo.rvalToLval.keys():
            if self.rvalContainsSymOfInterest(rval, symOfInterest):
                for lval in self.trackingInfo.rvalToLval[rval]:
                    expr = self.replaceLvalByVAR(expr, lval)
        
        # replace symbol of interest by $VAR
        reExpr = '(?<!\w)(%s)(?!\w)' % (re.escape(symOfInterest))
        expr = re.sub(reExpr, '$VAR', expr)
        
        return [expr]
    
   
    
    def replaceSymbol(self, symbol, replacement, expr):
        reExpr = '(?<!\w)(%s)(?!\w)' % (re.escape(symbol))
        expr = re.sub(reExpr, replacement , expr)
        return expr
    
    def rvalContainsSymOfInterest(self, rval, symOfInterest):
        return self.containsSymbol(rval, symOfInterest)
    
    def containsSymbol(self, haystack, needle):
        reExpr = '(?<!\w)(%s)(?!\w)' % (re.escape(needle))
        return re.search(reExpr, haystack)

    
    def replaceLvalByVAR(self, expr, lval):
        reExpr = '(?<!\w)(%s)(?!\w)' % (re.escape(lval))
        return re.sub(reExpr, '$VAR', expr)
