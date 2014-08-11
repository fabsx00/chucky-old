
import itertools

class SymbolPropagator:
    
    def propagate(self, trackingInfo, symbol, symbolType):
        self.symbolType = symbolType
        return self.propagateSymbol(trackingInfo, symbol)
    
    def propagateSymbol(self, trackingInfo, s):
        
        expanded = []
        symbols = self._propagateSymbol(trackingInfo, s, expanded)
        
        symbols = self.uniq(symbols)
        symbols = [x for x in symbols if x != None]
        return symbols

    def addAllOtherParameters(self, s, symbols, trackingInfo, expanded):
        
        for paramSymbol in trackingInfo.parameters:
            if paramSymbol == s: continue
            if paramSymbol in expanded: continue

            if paramSymbol not in symbols:
                newSymbols = self._propagateSymbol(trackingInfo, paramSymbol, expanded)
                symbols.extend(newSymbols)

    def addAllArguments(self, symbols, arguments, trackingInfo, expanded):
        
        for argSymbol in arguments:
            if argSymbol not in symbols:
                if argSymbol in expanded: continue
                newSymbols = self._propagateSymbol(trackingInfo, argSymbol, expanded)
                symbols.extend(newSymbols)

    
    def _propagateSymbol(self, trackingInfo, s, expanded):
        symbols = [s]
        expanded.append(s)
        
        # if symbol is a parameter, include all other parameters
        # if s in trackingInfo.parameters:
        #    self.addAllOtherParameters(s, symbols, trackingInfo, expanded)
            
        # if symbol is a function call, add all fields in arguments
        if s in trackingInfo.functionArguments:
            arguments = trackingInfo.functionArguments[s]
            self.addAllArguments(symbols, arguments, trackingInfo, expanded)
    
        # if symbol is used as an argument to a function, add that function
        # if s in trackingInfo.functionsConsuming:
        #    funcsToAdd = trackingInfo.functionsConsuming[s]
        #    # misnomer: should be addAllFuncs but it does the same
        #    self.addAllArguments(symbols, funcsToAdd, trackingInfo, expanded)
            
        # Include lvalues as 'symbols of interest'
        if trackingInfo.rvalToLval.has_key(s):
            lvals = trackingInfo.rvalToLval[s]
            for lval in lvals:
                if lval in expanded: continue
                symbols.extend(self._propagateSymbol(trackingInfo, lval, expanded))
            symbols.extend(lvals)
        
        # Include rvalues as 'symbols of interest'
        if trackingInfo.lvalToRval.has_key(s):
            rvals = trackingInfo.lvalToRval[s]
            for rval in rvals:
                if rval in expanded: continue
                symbols.extend(self._propagateSymbol(trackingInfo, rval, expanded))
            symbols.extend(rvals)

        return symbols
    
    """
    The 'interpretations code below is currently not used anymore
    but I left it here for reference'
    """
    
    def getInterpretations(self, symbols, symbolOfInterest):
        d = {}
        for s in symbols:
            d[s] = [str(s), '$VAR']
            
            rvalNodes = self.getRExpressionsForSymbol(s) 
            rvals = [node.row[1] for node in rvalNodes]
            d[s].extend(rvals)
            
        x = itertools.product(*[x for x in d.itervalues()])
        return x
    
    def getRExpressionsForSymbol(self, s):
        try:
            rvalNodes = self.trackingInfo.lvalToExpr[s]
            return rvalNodes
        except:
            return []
    
    def applyInterpretations(self, exprStr, interpretations, symbols):
        expressions = []
        
        # print len(symbols)
        # print symbols

        for interp in interpretations:
            i = 0
            newExprStr = exprStr
            for symbol in symbols:
                replacement = interp[i]
                if replacement != symbol:
                    newExprStr = self.replaceSymbol(symbol, replacement, newExprStr)
                
                expressions.append(newExprStr)
                i += 1
            
        return expressions

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