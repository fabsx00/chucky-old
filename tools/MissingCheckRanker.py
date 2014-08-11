
import cPickle as pickle

from MissingChecks import main as MissingChecksMain
from tools.functionAnomaly.RankingEntry import RankingEntry
from libjoern.index.FunctionIndex import FunctionIndex

def main(projectRoot, kmin, kmax, tau, symbolsOfInterest):
        
    ranking = []
    
    root = projectRoot + 'parsed'
    functionIndex = FunctionIndex(root)
    
    locationIter = functionIndex.getLocationIterator()
    
    for location in locationIter:
            
            # ADDED FOR EVAL
            if location.find('/t.c/') == -1: continue
            # if location.find('/msn/') == -1: continue
            #
            
            location = projectRoot + 'parsed/' + location
            contexts = MissingChecksMain(projectRoot + 'parsed/', location, kmin, kmax, tau, symbolsOfInterest)
              
            entry = functionAnomaliesToRankingEntry(location, contexts)
            ranking.append(entry)
            
            
    ranking.sort(reverse=True)
    pickle.dump(ranking, file(projectRoot + 'gammaCRanking.pickl', 'w'))

def functionAnomaliesToRankingEntry(location, contexts):
    return newFunctionAnomaliesToRankingEntry(location, contexts)
    # return oldFunctionAnomaliesToRankingEntry(location, contexts)
    
def newFunctionAnomaliesToRankingEntry(location, contexts):
    
    # Select the highest deviation from those models,
    # which have a confidence (, i.e. number of members)
    # of at least MIN_CONFIDENCE
    MIN_CONFIDENCE = 3
    
    maxGammaC = 0
    curNVoters = 0
    
    for context in contexts.itervalues():
        nVoters = len(context.neighbours)
        if nVoters >= MIN_CONFIDENCE:
            if context.gammaC != None and context.gammaC >= maxGammaC:
                if context.gammaC == maxGammaC:
                    if nVoters > curNVoters:
                        curNVoters = nVoters
                else:
                
                    maxGammaC = context.gammaC
                    curNVoters = nVoters

    return RankingEntry((maxGammaC,curNVoters) , location)
    
    
    # weighted average deviation from model
    # weights are model quality, i.e. number of voters
    
    # import numpy as np
    # nNeighbours = [len(c.neighbours) for c in contexts.itervalues()]
    # c = 1.0 / float(np.sum(nNeighbours))
    # weightedSum = c* (np.sum([len(c.neighbours) * c.gammaC for c in contexts.itervalues()]))
    # return RankingEntry(weightedSum, location)
    

def oldFunctionAnomaliesToRankingEntry(location, contexts):
    # Select the highest deviation score from those
    # symbols, which had the highest voter participation
    maxGammaC = 0
    maxNVoters = 0
    for context in contexts.itervalues():
        nVoters = len(context.neighbours)
        if nVoters > maxNVoters:
            maxNVoters = nVoters
            maxGammaC = context.gammaC
            continue
        elif nVoters == maxNVoters:
            if context.gammaC != None and context.gammaC > maxGammaC:
                maxGammaC = context.gammaC
    return RankingEntry(maxGammaC, location)
 
if __name__ == '__main__':
    import sys, ast
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    
    
    symbolsOfInterest = None
    try:
        kmin = int(sys.argv[2])
        kmax = int(sys.argv[3])
        tau = float(sys.argv[4])
    except:
        print 'specify kmin, kmax, tau'
        sys.exit()
    
    try:
        print sys.argv[5]
        symbolsOfInterest = ast.literal_eval(sys.argv[5])
        symbolsOfInterest = [str(x) for x in symbolsOfInterest]
        if symbolsOfInterest == None or symbolsOfInterest == []:
            print 'Error'
            sys.exit()
    except:
        pass
    
    print 'FOO: kmin, kmax, tau: %d %d %f' % (kmin, kmax, tau) 
    print 'Symbols of Interest: %s' %(symbolsOfInterest)
    main(projectRoot, kmin, kmax, tau, symbolsOfInterest)
