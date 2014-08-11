#!/usr/bin/env python2


import argparse
import sys, os
import cPickle as pickle

import numpy

sys.path.append(os.getcwd())

from tools.SinkSnippetEmbedder.SinkUserProvider import SinkUserProvider
from mlutils.anomalyDetection.anomalyCalculator import AnomalyCalculator
from mlutils.termDocMatrix.TermDocumentMatrix import TermDocumentMatrix

class GlitchFinder:
    
    def __init__(self):
        self._parseCommandLine()
        self._initializeFilesystemLocations()
    
    def _parseCommandLine(self):
        self._initializeCommandLineParser()
        self.args = self.parser.parse_args()
        
    def _initializeCommandLineParser(self):
        self.parser = argparse.ArgumentParser(description=
                                              'glitchFinder finds and highlights deviations from common programming patterns.')
        self.parser.add_argument('embeddingDir', type=str,
                                 help='The embedding directory containing the term by document matrix')
        
        self.parser.add_argument('sink', nargs='?', default=None,
                                 help='The sink to analyze. If this argument is not specified or does not exist,\
                                 glitchFinder will output the list of available sinks.')
        
        self.parser.add_argument('--min-calls-to-sink', '-m', default = 10)
        
        self.parser.add_argument('--cluster-algo', '-c', default='NIMFA_NMF')
        
    
    def _initializeFilesystemLocations(self):
        
        self.embeddingDir = self.args.embeddingDir
        if self.embeddingDir[-1] != '/': self.embeddingDir += '/'
        self.globalTermDocMatrixFilename = self.embeddingDir + 'termDocMatrix.pickl'
        self.projectRoot = '/'.join(self.embeddingDir.split('/')[:-3]) + '/'
    
    def run(self):
        
        self.sinks = self._getAvailableSinks()
        
        if not self.args.sink:
            self.outputAvailableSinks()
            return
    
        self._checkSink(self.args.sink)
        self.findGlitchesForSink(self.args.sink)
    
    
    def _getAvailableSinks(self):
        sinkUserProvider = SinkUserProvider(self.projectRoot)
        return sinkUserProvider.getSinks(self.args.min_calls_to_sink)

    def outputAvailableSinks(self):   
        sinkSummary = self._createSinkSummary(self.sinks)
        for entry in sinkSummary:
            print '"%s",%d' % (entry[1], entry[0])

    def _checkSink(self, sink):
        sinkNames = self._getSinkNamesFromSinks(self.sinks)
        if sink in sinkNames: return
        print 'Error: sink not found'
        sys.exit(1)
    
    def _getSinkNamesFromSinks(self, sinks):
        return [s[0] for s in sinks]
    
    
    def findGlitchesForSink(self, sink):
        if self.args.cluster_algo in ['NIMFA_NMF', 'SVD']:
            self.SVDNMFFindGlitchesForSink(sink)
    
    def SVDNMFFindGlitchesForSink(self, sink):
        termDocMatrix = self._getTermDocMatrixForSink(sink)
        
        from mlutils.clustering.NMFCluster import NMFCluster
        nmfCluster = NMFCluster()
        nmfCluster.algorithm = self.args.cluster_algo
        nmfCluster.cluster(termDocMatrix)
                
        self.outputClusterStatistics(nmfCluster)
        
        anomalyResults = self.anomalyDetection(nmfCluster)
        
        print 'Global Anomaly Ranking:'
        for r in anomalyResults: print r
        
        self.outputCode(anomalyResults, nmfCluster)
    
    def outputCode(self, anomalyResults, nmfCluster):
        from FunctionPrinter import FunctionPrinter
        functionNames = [l[1] for l in anomalyResults]
        for location in functionNames:
            FunctionPrinter().printFunction(location, nmfCluster)
        
    
    def _getTermDocMatrixForSink(self, sink):
        self._loadGlobalTermDocMatrix()
        termDocMatrix = self._createTermDocMatrixForSink(sink)
        # save
        return termDocMatrix
    
    def _loadGlobalTermDocMatrix(self):
        filename = self.globalTermDocMatrixFilename
        self.globalTermDocMatrix = pickle.load(file(filename))
    
    def anomalyDetection(self, nmfCluster):
        
        anomalyCalculator = AnomalyCalculator()
       
        docs = nmfCluster.H
        nDocs = docs.shape[1]
        labels = nmfCluster.labels
        
        # scores = anomalyCalculator.anomalyAnalysis(docs, nDocs)
        scores = self.determineNMFErrorVecs(nmfCluster)
        anomalyResults = [(scores[i], labels[i]) for i in range(nDocs)]
        anomalyResults.sort(reverse=True)
        
        return anomalyResults

    def determineNMFErrorVecs(self, nmfCluster):
        E = nmfCluster.getError()
        scores = (numpy.square(E).sum(axis=0)).tolist()[0]
        return scores

      
    def outputClusterStatistics(self, nmfCluster):
        print 'Number of clusters: %d' % (nmfCluster.getNumberOfClusters())
        print 'Cluster Statistics:'
        print 'Score, Average Distance, Number of members, ClusterIndex'
        for (score, avgDistance, clusterIndex, nMembers) in nmfCluster.calculateInnerClusterDistances():
            print '%f, %f, %d, %d' % (score, avgDistance, nMembers, clusterIndex)
        
        print 'Clusters:'
        nmfCluster.printClusterDict()
        print '============='
        
        prototypes = nmfCluster.getPrototypes(0.05)
        for p in prototypes:
            print '--- Vector ---'
            for r in p: print r
    
    def _getFunctionNamesFromSink(self, sinkName):
        sinkUserProvider = SinkUserProvider(self.projectRoot)
        sink = sinkUserProvider.getSinkByName(sinkName)
        (unused, callsToSink) = sink
        functionNames = self.unique([self.projectRoot + c[1] for c in callsToSink])
        return functionNames
     
    def _createTermDocMatrixForSink(self, sinkName):
        
        functionNames = self._getFunctionNamesFromSink(sinkName)
        
        colIndices = [self.globalTermDocMatrix.doc2Index[f] for f in functionNames]
        matrix = self.globalTermDocMatrix.matrix.tocsc()
        
        newIndex2Doc = functionNames
        newDoc2Index = {}
        for i in xrange(len(functionNames)):
            newDoc2Index[functionNames[i]] = i
        
        newMatrix = matrix[:,colIndices].tolil()
        newTermDocMatrix = TermDocumentMatrix()
        newTermDocMatrix.matrix = newMatrix
        newTermDocMatrix.index2Doc = newIndex2Doc
        newTermDocMatrix.doc2Index = newDoc2Index
        newTermDocMatrix.term2Index = self.globalTermDocMatrix.term2Index
        newTermDocMatrix.index2Term = self.globalTermDocMatrix.index2Term
        newTermDocMatrix.nterms = len(newTermDocMatrix.index2Term)
        return newTermDocMatrix
    
    def unique(self, seq, idfun=None): 
        # order preserving
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result

    
    def _createSinkSummary(self, sinks):
        sinkSummary = []
        for sink in sinks:
            sinkName = sink[0]
            callsToSink = sink[1]
            summaryEntry = (len(callsToSink), sinkName)
            sinkSummary.append(summaryEntry)
        
        sinkSummary.sort(reverse=True)
        return sinkSummary

def main():
    glitchFinder = GlitchFinder()
    glitchFinder.run()


if __name__ == '__main__':
    main()
