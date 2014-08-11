
from Ranker import Ranker

class TermDocMatrixRanker(Ranker):
    
    def rank(self, anomalyScore, k):
        self.loadTermDocMatrix()
        self.loadDistanceMatrix()

        scores = self.determineAnomaliesFromDistanceMatrix(anomalyScore, k)
        ranking = self.rankingFromScores(scores)
        return ranking