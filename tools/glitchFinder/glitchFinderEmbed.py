#!/usr/bin/env python2
import argparse, os, sys

sys.path.append(os.getcwd())

from mlutils.ngramEmbedding.create import  embedFunctions
from mlutils.termDocMatrix.create import main as createTermDocMatrix
from mlutils.sinkMatrix.create import main as sinkEmbed

class GlitchFinderEmbed:
    def __init__(self):
        self._parseCommandLine()
    
    def _parseCommandLine(self):
        self._initializeCommandLineParser()
        self.args = self.parser.parse_args()
        
    def _initializeCommandLineParser(self):
        self.parser = argparse.ArgumentParser(description=
                                              'glitchFinderEmbed performs different embeddings for glitchFinder')
        
        self.parser.add_argument('projectDirectory', type=str,
                                 help='The glitchFinder project directory created by glitchFinderImport.')
        
        self.parser.add_argument('sink', nargs='?', default=None)
         
        self.parser.add_argument('--ngram-n', '-n', default=1, type=int,
                                 help='Length of n-grams to consider.')
        
        self.parser.add_argument('--smaller-ngrams-too', '-s', action="store_true", default=False,
                                 help='Include ngrams up to a specified length as opposed to only ngrams of a specified length')

        self.parser.add_argument('--tfidf', '-t', action="store_true", default=False,
                                 help='Perform tf-idf term-weighing')

        self.parser.add_argument('--filter', '-f', default = 'DefaultFilter')

        self.parser.add_argument('--min-calls-to-sink', '-m', default = 20)


    def run(self):
        self.ngramEmbed()
        self.createTermDocumentMatrix()
        # self.embedSinks()
        
    def ngramEmbed(self): 
        projectRoot = self.args.projectDirectory
        print 'Creating Ngram-Embedding for %s' % (projectRoot)
        
        self.embeddingDir = projectRoot + 'embeddings/%s_%d.pickl/' % (self.args.filter, self.args.ngram_n)
        # if os.path.exists(self.embeddingDir):
        #    print 'Skipping global embedding, it already exists.'
        #    return
           
        filterName = self.args.filter
        ngramN = self.args.ngram_n
        smallerNgramsToo = self.args.smaller_ngrams_too
        sink = self.args.sink
        embedFunctions(projectRoot, filterName, ngramN, smallerNgramsToo, sink)
    
    def createTermDocumentMatrix(self):
        print 'Creating Term by Document Matrix in %s' % (self.embeddingDir)
        createTermDocMatrix(self.embeddingDir, self.args.tfidf)
    
    def embedSinks(self):
        self.sinks = self._getAvailableSinks()
        for (sinkName, unused) in self.sinks:
            sinkEmbed(self.embeddingDir, sinkName)
        
    def _getAvailableSinks(self):
        from tools.SinkSnippetEmbedder.SinkUserProvider import SinkUserProvider
        sinkUserProvider = SinkUserProvider(self.args.projectDirectory)
        return sinkUserProvider.getSinks(self.args.min_calls_to_sink)
    
    
    # Taken out for now
    def factorize(self):
        from mlutils.factorization.create import main as factorize
        rank = 0
        factorize(self.embeddingDir, rank, self.args.matrix_factorization)
    
    
if __name__ == '__main__':
    glitchFinderEmbed = GlitchFinderEmbed()
    glitchFinderEmbed.run()
    