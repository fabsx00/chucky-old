
import cPickle as pickle
import numpy

from mlutils.ngramEmbedding.Embedder import Embedder
from mlutils.termDocMatrix.NameDictMapToMatrix import NameDictMapToMatrix

from SinkSnippetExtractor import SinkSnippetExtractor

UPPER_BOUND_FOR_NUMBER_OF_CALLS_AS_FRACTION = 0.05
LOWER_BOUND_FOR_NUMBER_OF_CALLS = 1


class SinkSnippetEmbedder:

    def __init__(self, projectRoot, ngramN, smallerNgramsToo):
        
        self.projectRoot = projectRoot
        self.nCalls = self._determineTotalNumberOfCalls()
        
        self.callAreaExtractor = SinkSnippetExtractor()
        self.embedder = Embedder(projectRoot)
        self.embedder.configureNgramCalculator(ngramN, smallerNgramsToo)
        self.nameDictMapToMatrix = NameDictMapToMatrix()
   
    def _isSinkCalledTooOften(self, callsToSink):
        # If more than 50 percent of calls are calls to
        # this function, this sink is just called to often
        # to be interesting
        if float(len(callsToSink))/self.nCalls > UPPER_BOUND_FOR_NUMBER_OF_CALLS_AS_FRACTION:
            print 'Sink called too often'
            return True
        return False
    
    def _isSinkNotCalledOftenEnough(self, callsToSink):
        return (len(callsToSink) < LOWER_BOUND_FOR_NUMBER_OF_CALLS)
    
    def _determineTotalNumberOfCalls(self):
        callIndex = pickle.load(file(self.projectRoot + 'callIndex.pickl'))
        return numpy.sum([len(v) for v in callIndex.d.itervalues()])
        
    def embedSinkUsers(self, sink):
        
        callsToSink = sink[1]
        
        if self._isSinkCalledTooOften(callsToSink):
            return (None, None)
        if self._isSinkNotCalledOftenEnough(callsToSink):
            print 'Sink not called often enough'
            return (None, None)
        
        getSinkAreaSubtree = self.callAreaExtractor.getSinkAreaSubtree
        filterAndAddAST = self.embedder.filterAndAddAST
        
        for label in callsToSink:
            areaSubtree = getSinkAreaSubtree(self.projectRoot, label)    
            filterAndAddAST(label, areaSubtree)
        
        (vecs, allNgrams) = self.embedder.getMaps()
        self.nameDictMapToMatrix.convertFromDicts(vecs, allNgrams)
        return (sink[0], self.nameDictMapToMatrix.termDocumentMatrix)
    
    def save(self, name, sinkName):
        import os
        
        embeddingsDir = self.projectRoot + 'embeddings'
        thisEmbeddingDir = embeddingsDir + '/'+ name
        sinkEmbeddingDir = thisEmbeddingDir + '/' + 'sinks'
        thisSinkEmbeddingDir = sinkEmbeddingDir + '/' + sinkName
        
        if not os.path.exists(embeddingsDir):
            os.mkdir(embeddingsDir)
        
        if not os.path.exists(thisEmbeddingDir):
            os.mkdir(thisEmbeddingDir)
        
        if not os.path.exists(sinkEmbeddingDir):
            os.mkdir(sinkEmbeddingDir)
        
        if not os.path.exists(thisSinkEmbeddingDir):
            os.mkdir(thisSinkEmbeddingDir)
            
        pickle.dump(self.nameDictMapToMatrix.nameDictMap, file( thisSinkEmbeddingDir + '/func2SubtreesMap.pickl', 'w'))
        pickle.dump(self.nameDictMapToMatrix.allSymbolsDict, file( thisSinkEmbeddingDir + '/allSubtreesDict.pickl', 'w'))
    
    