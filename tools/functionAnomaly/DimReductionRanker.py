
from Ranker import Ranker
from mlutils.clustering.NMFCluster import NMFCluster
import numpy

class DimReductionRanker(Ranker):
    
    def clusterTermDocMatrix(self, initialNBases=200, algorithm='SVD'):
        self.nmfCluster = NMFCluster()
        self.nmfCluster.algorithm = algorithm
        self.initialNBases = initialNBases
        self.nmfCluster.cluster(self.termDocMatrix, self.initialNBases)
        print 'W: %d, %d' % (self.nmfCluster.W.shape[0], self.nmfCluster.W.shape[1])
    
    def determineNMFErrorVecs(self):
        E = self.nmfCluster.getError()
        scores = (numpy.square(E).sum(axis=0)).tolist()[0]
        return scores

    def rank(self, initialNBases = 200, algorithm='SVD'):
        self.loadTermDocMatrix()
        self.clusterTermDocMatrix(initialNBases, algorithm)
        scores = self.determineNMFErrorVecs()
        ranking = self.rankingFromScores(scores)
        return ranking
        