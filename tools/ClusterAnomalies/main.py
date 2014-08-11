from tools.SinkSnippetEmbedder.SinkUserProvider import SinkUserProvider
from tools.SinkSnippetEmbedder.SinkSnippetEmbedder import SinkSnippetEmbedder

from mlutils.clustering.NMFCluster import NMFCluster
from mlutils.anomalyDetection.anomalyCalculator import AnomalyCalculator

from tools.ClusterAnomalies.Configurations.DefaultConfiguration import DefaultConfiguration

from mlutils.editDistanceEmbedding.createDistanceMatrix import distanceMatrixFromLocations

import sys, pickle, numpy

def usage():
    print '<projectRoot> <sinkOfInterest> [outputFilename]'

def sinkSnippetEmbedder(projectRoot, sinkOfInterest, configuration):
    
    print 'embed for sink: %s' % sinkOfInterest
    sink = SinkUserProvider(projectRoot).getSinkByName(sinkOfInterest)
    sinkUserEmbedder = SinkSnippetEmbedder(projectRoot, configuration['ngramN'], configuration['smallerNgramsToo'])
    (name, termDocMatrix) = sinkUserEmbedder.embedSinkUsers(sink) #@UnusedVariable
    return termDocMatrix
    
def anomalyDetection(projectRoot, nmfCluster):
    from sklearn.metrics.pairwise import pairwise_distances
    
    anomalyCalculator = AnomalyCalculator()
    anomalyResults = []
    
    numberOfClusters = nmfCluster.getNumberOfClusters()
    for clusterId in range(numberOfClusters):
        (clusterMatrixLabels, clusterMatrix) = nmfCluster.getLowerDimensionalMatrixForCluster(clusterId)
        
        # editDistances = distanceMatrixFromLocations(projectRoot, clusterMatrixLabels)
        # if editDistances == None: continue
        
        nDatapointsInCluster = clusterMatrix.shape[1]
        if clusterMatrix.shape[0] > 0 and clusterMatrix.shape[1] > 0:
            averageDistanceInCluster = numpy.mean(pairwise_distances(clusterMatrix.T))
        else:
            averageDistanceInCluster = 0
        
        (gammaScores,zetaScores) = anomalyCalculator.anomalyAnalysis(clusterMatrix, nDatapointsInCluster)
        # (gammaScores, zetaScores) = anomalyCalculator.analyzeDistanceMatrix(editDistances, k=100)
        
        # distToPrototype = anomalyCalculator.dist2Prototype(nmfCluster.getPrototype(clusterId) , clusterMatrix)
        # D = [(gammaScores[i], zetaScores[i], distToPrototype[i], clusterMatrixLabels[i]) for i in range(len(clusterMatrixLabels))]
        D = [(gammaScores[i]  , averageDistanceInCluster, 0, clusterMatrixLabels[i]) for i in range(len(clusterMatrixLabels))]
        # D = [(gammaScores[i], clusterMatrixLabels[i]) for i in range(len(clusterMatrixLabels))]
        D.sort(reverse=True)
        anomalyResults.append(D)
        
    return anomalyResults

def main(projectRoot, sinkOfInterest, outputFilename, configuration):
    
    nmfCluster = NMFCluster(configuration)
    
    
    termDocMatrix = sinkSnippetEmbedder(projectRoot, sinkOfInterest, configuration)
    if termDocMatrix == None:
        print 'termDocMatrix empty'
        return
    
    nmfCluster.cluster(termDocMatrix)
    # basis_vector_printing_thresh = 0.1
    # nmfCluster.printPrototypes(basis_vector_printing_thresh)
    anomalyResults = anomalyDetection(projectRoot, nmfCluster)
    
    if outputFilename != None:
        pickle.dump(anomalyResults, file(outputFilename, 'w'))

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    
    if len(sys.argv) >= 3:
        sinkOfInterest = sys.argv[2]
    else:
        sinkOfInterest = None
    
    if len(sys.argv) == 4:
        outputFilename = sys.argv[3]
    else:
        outputFilename = None
    
    main(projectRoot, sinkOfInterest, outputFilename, DefaultConfiguration())
