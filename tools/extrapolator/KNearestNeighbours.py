import sys, math, pickle, scipy
import scipy.sparse
import numpy

class KNearestNeighbours():
    def __init__(self):
        pass
    
    def initialize(self, pickleDir):
        if pickleDir[-1] == '/': pickleDir = pickleDir[:-1]
        self.termDocMatrix = pickle.load(file('%s/termDocMatrix.pickl' % (pickleDir), 'rb'))
        self.H = pickle.load(file('%s/H.pickl' % (pickleDir), 'rb'))
        
    def getKNearestNeighbours(self, funcnameRe, n=200):
        
        q = self.getVectorForRegex(funcnameRe)
        return self.getSimilarToVector(q, n)
    
    def getVectorForRegex(self, funcnameRe):
        
        doc2Index = self.termDocMatrix.doc2Index
        matchingFuncs = [k for k in doc2Index.keys() if funcnameRe.search(k)]
        
        if len(matchingFuncs) == 0: return
        if len(matchingFuncs) != 1:
            print 'Be more precise, more than one function matches.'
            print matchingFuncs
            return None
        
        m = matchingFuncs[0]
        return self.H[:,doc2Index[m]]
        
    
    def getSimilarToVector(self, q, n=100):
        index2Doc = self.termDocMatrix.index2Doc        
         
        distances = self.cosineDistances(self.H, q)
        # distances = self.euclideanDistance(self.H, q)
        
        iDistances = [(distances[i], index2Doc[i]) for i in range(len(distances))]
        iDistances.sort(reverse=True)
        if n != 0:
            return iDistances[1:n+1]
        else:
            return iDistances

    def euclideanDistance(self, H, q):
        return [numpy.sum((h - q)**2) for h in self.H.T]

    def cosineDistances(self, H, q):
        lenQ = math.sqrt(q.dot(q))
        e = 0.00000001 # make sure we don't divide by 0.
        return [ h.dot(q)/(lenQ * math.sqrt(h.dot(h)) + e )  for h in self.H.T]

