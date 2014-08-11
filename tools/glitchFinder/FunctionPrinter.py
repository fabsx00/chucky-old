import numpy

class FunctionPrinter:
    
    def printFunction(self, location, nmfCluster):
        
        import ast
        prototypes = nmfCluster.getPrototypes(0.05)
        patternNgrams = []
        for p in prototypes:
            patternNgrams.extend([e[1] for e in p])
        
        patternTerms = []
        for ngram in patternNgrams:
            patternTerms.extend(ast.literal_eval(ngram))
        
        patternTerms = self.unique([p for p in patternTerms if p != ''])
         
        f = file(location + '/func_ast.csv')
        parsedInfo = f.readlines()
        functionRow = parsedInfo[0][:-1].split('\t')
        f.close()
        
        # tokendict
        tokenDict = {}
        for row in parsedInfo[1:]:
            row = row[:-1].split('\t') 
            startLine = int(row[1].split(':')[0])
            endLine = int(row[2].split(':')[0])
                        
            if len(row) < 5: continue
            if startLine == 0: continue
            if endLine == 0: endLine = startLine
                        
            for i in range(startLine, endLine + 1):
                try:
                    tokenDict[i-1].append(row[4])
                except:
                    tokenDict[i-1] = [row[4]]
        
                
        startLine = int(functionRow[1].split(':')[0])
        endLine = int(functionRow[2].split(':')[0])
        
        f = file(location + '/../source')
        code = f.readlines()
        f.close()
        
        print location
        for i in xrange(startLine,endLine):
            line = code[i]
            
            if tokenDict.has_key(i):
                for term in patternTerms:              
                    if term in tokenDict[i]:
                        # print 'TERM: ' + term
                        
                        j = line.find(term)
                        if j == -1: continue
                        line = line[:j] + "\033[95m" + line[j:j+len(term)] + "\033[0m" + line[j+len(term):]

            print line,
    
    def unique(self, seq, idfun=None): 
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
        