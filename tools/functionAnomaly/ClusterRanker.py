
from Ranker import Ranker
from tools.ClusterAnomalies.rank import normalize, averageRanking

class ClusterRanker(Ranker):

    def __init__(self, projectRoot):
        Ranker.__init__(self, projectRoot)

    def outputClusters(self, clusters):
        for cluster in clusters:
            print ' ==== Cluster ====='
            for member in cluster:
                print member

    def rankingFromClusters(self, clusters):
        ranking = []
        for cluster in clusters:
            cluster = self.reorderInCluster(cluster)
            cluster = normalize(cluster)
            print ' ==== Cluster ====='
            for member in cluster:
                print member
                ranking.append(member)
        ranking.sort(reverse=True)
        return averageRanking(ranking)
    
    def reorderInCluster(self, cluster):
        nMembers = len(cluster)
        
        cluster = [(self.skewFunc(cluster[i][0], i, nMembers), cluster[i][1], cluster[i][2], cluster[i][3]) for i in xrange(len(cluster))]
        cluster.sort(reverse=True)
        return cluster
    
    def skewFunc(self, score, x, nMembers):
        return score
    
    def rankingFromClustersDrawMethod(self, clusters):
        outliers = [c for c in clusters if len(c) <= 0]
        clusters = [(len(c), -c[0][0], c) for c in clusters if len(c) > 0]
        
        clusters.sort()
        clusters = [c[2] for c in clusters]
        
        globalRanking = []
        
        while len(clusters) != 0:
            currentCluster = clusters.pop(0)
            if len(currentCluster) == 0:
                continue
            globalRanking.append(currentCluster.pop(0))
            if len(currentCluster) != 0:
                clusters.append(currentCluster)
            
        for outlierCluster in outliers:
            for member in outlierCluster:
                globalRanking.append(member)
        
        ranking = averageRanking(globalRanking)
        return ranking