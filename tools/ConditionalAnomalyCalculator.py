import numpy
from sourceutils.expressionTrees.ExpressionTreeEmbedder import ExpressionTreeEmbedder

class ConditionalAnomalyCalculator:
    
    def __init__(self):
        self.exprTreeEmbedder = ExpressionTreeEmbedder()
        
    def conditionalAnomaly(self, contextsForFunction):
                
        for context in contextsForFunction.itervalues():
            
            termDocMatrix = self.exprTreeEmbedder.embed(context, context.symbol)
            if termDocMatrix == None:
                continue
            # Results are written into the context object
            # That's not really good.
            self.calculateDeviationVector(context, termDocMatrix)
    
    def calculateDeviationVector(self, context, termDocMatrix):

        originLocation = context.origin.location
        matrix = termDocMatrix.matrix.tocsc()
        originDocIndex = termDocMatrix.doc2Index[originLocation]
        originFunctionVector = matrix[:,originDocIndex]
        xd = originFunctionVector.todense()
        
        vectors = []
        distances = [] # distance in API space
        cDistances = [] # distance in expression space
        
        # Add self to model
        # vectors.append(originFunctionVector.T)
        # distances.append(0.0)
        # cDistances.append(0.0)
        #
        
        for neighbour in context.neighbours:
            l = neighbour.location
            vectors.append(matrix[:,termDocMatrix.doc2Index[l]].T)
            distances.append(neighbour.distance)
            neighbourVec = vectors[-1].todense().T
            cDistances.append(self.cosineDistance(xd, neighbourVec))
                
        mue = self.calculateWeightedMean(vectors, distances)
         
        context.gammaC = (1.0/(len(cDistances))) * numpy.sum(cDistances)
        # alpha = [(1-d) for d in distances]
        # N = numpy.sum(alpha)
        # context.gammaC = (1.0/N) * numpy.sum([alpha[i]*cDistances[i] for i in xrange(len(cDistances))])
                        
        context.gammaA = float(numpy.sum(distances)) / len(distances)
        context.mue = mue
        context.originVector = originFunctionVector.T
        context.deviationVec = originFunctionVector.T - mue
        context.index2Term = termDocMatrix.index2Term
        
        # From the deviation vector, take all negative coefficients
        # Then calculate the length of the resulting vector
        
        # context.gammaC = self.euclideanDev(context.deviationVec)
        context.gammaC = self.maxDev(context.deviationVec) 
        
        # Finally, weigh by (1-gammaA) to account for the quality of neighbours
        # context.gammaC *=  (1.0 - context.gammaA) 
      
    def cosineDistance(self, x ,y):
        from scipy.spatial.distance import cosine
        from numpy.linalg import norm
        if norm(x) == 0 or norm(y) == 0:
            if norm(x) == norm(y):
                return 0.0
            else:
                return 1.0
        return cosine(x,y)
            
    def euclideanDev(self, deviationVec):
        missing = [i**2 for i in deviationVec.toarray()[0,:] if i < 0]
        return numpy.sum(missing)
    
    def maxDev(self, deviationVec):
        # missing = [i**2 for i in deviationVec.toarray()[0,:] if i < 0]
        missing = [float(-i) for i in deviationVec.toarray()[0,:] if i < 0]
        if len(missing) == 0:
            return 0
        return numpy.max(missing)
    
        
    def calculateWeightedMean(self, vectors, distances):
        # N = numpy.sum([1-d for d in distances])
        # mue = numpy.sum([(1-d) * v for (v,d) in zip(vectors, distances)])
        N = len(distances)        
        mue = numpy.sum([v for (v,d) in zip(vectors, distances)])
        mue *= (1.0/N)
        return mue
