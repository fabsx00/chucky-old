import pickle
from scipy.spatial.distance import squareform
import os

from mlutils.anomalyDetection.anomalyCalculator import AnomalyCalculator
from RankingEntry import RankingEntry


class Ranker:
    def __init__(self, projectRoot):
        self.projectRoot = projectRoot
        
    def loadTermDocMatrix(self):
        termDocMatrixFilename = self.projectRoot + 'termDocMatrix.pickl'
        self.termDocMatrix = pickle.load(file(termDocMatrixFilename))
        self.labels = self.termDocMatrix.index2Doc

    
    def loadDistanceMatrix(self):
      
        DFilename = self.projectRoot + 'D_euclidean.pickl'
        self.D = pickle.load(file(DFilename))
        if self._isCompressedDistanceMatrix(self.D):
            self.D = squareform(self.D)

    def _isCompressedDistanceMatrix(self, D):
        return len(D.shape) == 1

    def loadH(self):
        HFilename = self.projectRoot + 'H.pickl'
        self.H = pickle.load(file(HFilename))
        
    def rank(self):
        print 'Implement "rank()"'
        pass
    
    def outputRanking(self):
        for r in self.ranking: print r
    
    def determineAnomaliesFromDistanceMatrix(self, anomalyScore, k):
        anomalyCalculator = AnomalyCalculator()
        scores = anomalyCalculator.analyzeDistanceMatrix(self.D, anomalyScore, k)
        return scores

    def rankingFromScores(self, scores):
        self.ranking = []
        for i in xrange(len(self.labels)):
            score = scores[i]
            label = self.labels[i]
            self.ranking.append(RankingEntry(score, label))
        
        self.ranking.sort(reverse=True)

    def saveRanking(self, filename):
        rankingsDir = self.projectRoot + 'rankings'
        if not os.path.exists(rankingsDir):
            os.mkdir(rankingsDir)
        
        outFilename = rankingsDir + '/' + filename
        pickle.dump(self.ranking, file(outFilename, 'w'))
        