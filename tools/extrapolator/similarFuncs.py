import pickle
import sys, re
import math, numpy, scipy.sparse

from KNearestNeighbours import KNearestNeighbours


def prettyPrintSimilarFuncs(simFuncs):
    pos = 1
    for (score, row) in simFuncs:
        print '%d %.2f & %s\\\\' % (pos, score, row)
        pos += 1

def buildCustomVector(self, query):
        terms = query.split('<>')
        customVector = None
        for term in terms:
            if customVector != None:
                customVector += self.W[self.termDocMatrix.term2Index[term], :]
            else:
                customVector = self.W[self.termDocMatrix.term2Index[term], :]
        
        return customVector
                        

def main():

    firstArgument = sys.argv[1]
    
    if len(sys.argv) == 3:
        projectRoot = sys.argv[2]
    else:
        projectRoot = '.pickle'

    s = KNearestNeighbours()
    s.initialize(projectRoot)
    
    if firstArgument[0] != '@':
        funcnameRe = re.compile(firstArgument)
        simFuncs = s.getKNearestNeighbours(funcnameRe)
    else:
        query = firstArgument
        q = s.buildCustomVector(query)
        print q
        simFuncs = s.getSimilarToVector(q)
    
    prettyPrintSimilarFuncs(simFuncs)
        
if __name__ == '__main__':
    main()
