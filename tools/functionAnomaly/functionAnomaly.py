
import sys
from TermDocMatrixRanker import TermDocMatrixRanker
from DimReductionRanker import DimReductionRanker

                
def clusterDictToSortedClusters(clusterDict):
    sortedClusters = []
    for v in clusterDict.itervalues():
        sortedClusters.append((len(v), v))
    sortedClusters.sort()
    return sortedClusters
    
def normalizeProjectRoot(projectRoot):
    if projectRoot[-1] != '/': projectRoot += '/'
    return projectRoot


def termDocMatrixRankings(projectRoot):
    for anomalyScore in ['gamma', 'zeta']:
        for k in [2,4,6,8,10,14,18,22,24,30,40,50,60]:
            ranker = TermDocMatrixRanker(projectRoot)
            ranker.rank(anomalyScore,k)
            ranker.saveRanking('termDocMatrixRanker_%s_%d.pickl' % (anomalyScore, k))
            # ranker.outputRanking()

def NMFErrorRankings(projectRoot):
    ranker = DimReductionRanker(projectRoot)
    ranker.rank()
    ranker.saveRanking('NMFErroRanker_SVD_200.pickl')
    
def main(projectRoot):
    termDocMatrixRankings(projectRoot)
    # NMFErrorRankings(projectRoot)
    
if __name__ == '__main__':
    projectRoot = normalizeProjectRoot(sys.argv[1])
    main(projectRoot)
    