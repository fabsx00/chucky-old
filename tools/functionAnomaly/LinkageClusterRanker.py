
from ClusterRanker import ClusterRanker
from mlutils.clustering.LinkageClustering import LinkageClustering

class LinkageClusterRanker(ClusterRanker):
    
    def clusterTermDocMatrix(self):
        matrix = self.termDocMatrix.matrix.tocsc()
        self._clusterMatrix(matrix)
        
    def clusterReducedMatrix(self):
        matrix = self.H
        self._clusterMatrix(matrix)
        
    def _clusterMatrix(self, matrix):
        linkageCluster = LinkageClustering(self.labels, matrix.tocsc())
        linkageCluster.cluster(self.D)
