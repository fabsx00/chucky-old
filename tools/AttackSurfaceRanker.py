
from tools.functionAnomaly.RankingEntry import RankingEntry
from tools.functionAnomaly.Ranker import Ranker
from sourceutils.misc.NameToDictMap import NameToDictMap
from mlutils.anomalyDetection.anomalyCalculator import AnomalyCalculator

import pickle
import numpy
import sys

def determineUncheckedIdentifiers():
    pass

def calculateF(CAllSubtrees):
    totalNumberOfChecks = numpy.sum((c for c in CAllSubtrees.d.itervalues()))
    print 'Total number of checks: %d'  % (totalNumberOfChecks)
    
    # normalized F
    F = CAllSubtrees.d
    for k in F.keys():
        F[k] = float(F[k]) / totalNumberOfChecks
        # F[k] = 1

    return F

def calculateCheckVectors(WFuncs, CFuncs, F, binary=True, alpha=1, weighByF = False):
    
    WDict = NameToDictMap()
    for (functionLocation, symbols) in WFuncs.d.iteritems():
        
        if not functionLocation in CFuncs.d:
            # The function does not contain any check,
            # thus, projected onto the check-space, it's
            # the NULL-vector
            WDict.d[functionLocation] = {}
            continue
        
        CFunc = CFuncs.d[functionLocation]
        
        for (s,occurrences) in symbols.iteritems():
            if binary: occurrences = 1
            
            if (not s in F):
                # This symbol is never checked
                WDict.setItem(s, functionLocation, 0)
            elif (s in CFunc):
                w = 1.0
                if weighByF: w = F[s]
                nChecks = CFunc[s]
                if binary: nChecks = 1
                WDict.setItem(s, functionLocation, (occurrences - alpha*nChecks)*w)
            else:
                w = 1.0
                if weighByF: w = F[s]
                WDict.setItem(s, functionLocation, occurrences*w)
    return WDict

def relevancyWeighting(checkVectors, featureDir):
    
    k = 20
    
    termDocMatrix = pickle.load(file(featureDir + 'termDocMatrix.pickl'))
    functionLocations = termDocMatrix.index2Doc

    # it doesn't make much sense that we use euclidean distances here,
    # should be L1, but I can't calculate L1 on the sparse matrices for now.
    from scipy.spatial.distance import squareform
    D = squareform(pickle.load(file(featureDir + 'D_euclidean.pickl')))
    anomalyCalculator = AnomalyCalculator()
    (NNV, NNI) = anomalyCalculator.calculateNearestNeighbours(k, D)
    
    WDict = NameToDictMap()
    for i in xrange(len(functionLocations)):
        
        location = functionLocations[i]
        if not location in checkVectors.d:
            continue
        
        WDict.d[location] = checkVectors.d[location]
        
        indices = NNI[:,i]
        gamma = float(numpy.sum(NNV[:,i]))/k
        locations = [functionLocations[j] for j in indices]       
        V = [checkVectors.d[l] for l in locations if l in checkVectors.d]
        distances = [NNV[j,i] for j in xrange(len(locations)) if locations[j] in checkVectors.d]
        
        # len(V) may be unequal to k if at least one of the nearest neighbours has no checks.
        # It is then a null-vector, so we're implicitly adding it in mean-calculation
        meanVector = {}
        for (v,d) in zip(V,distances):
            
            for (name, score) in v.iteritems():
                try:
                    meanVector[name] += (1-d)* (float(score)/k)
                except KeyError:
                    meanVector[name] = (1-d)* (float(score)/k)
        

        for (name, score) in checkVectors.d[location].iteritems():
            if meanVector.has_key(name):
                score -= meanVector[name]
                if score < 0: score = 0
                WDict.setItem(name, location, score)
    return WDict
        
def scoresFromCheckVectors(checkVectors):
    scores = []
    for (functionLocation, symbols) in checkVectors.iteritems():
        if len(symbols) == 0:
            score = 0
        else:
            X = [s for s in symbols.itervalues()]
            score = float(numpy.sum(X))
            score /= len(X)
        scores.append((score, functionLocation))
    return scores

def main(projectRoot):
    embedDir = projectRoot + 'embeddings/'
    waterOnlyDir = embedDir + 'WaterOnly_1.pickl/'
    identifiersInCondDir = embedDir + 'IdentifiersInConditions_1.pickl/'
    apiUsageDir = embedDir + 'APISymbols_1.pickl/'
       
    Wfunc2SubtreesFilename = waterOnlyDir + 'func2SubtreesMap.pickl'
    Cfunc2SubtreesFilename = identifiersInCondDir + 'func2SubtreesMap.pickl'
    CAllSubtreesFilename = identifiersInCondDir + 'allSubtreesDict.pickl'
    
    CAllSubtrees = pickle.load(file(CAllSubtreesFilename))
    CFuncs = pickle.load(file(Cfunc2SubtreesFilename))
    WFuncs = pickle.load(file(Wfunc2SubtreesFilename))
    
    if (len(WFuncs.d) < len(CFuncs.d)):
        print 'Error'
    
    
    print len(WFuncs.d)
    
    F = calculateF(CAllSubtrees)
    checkVectors = calculateCheckVectors(WFuncs, CFuncs, F)
    # checkVectors = relevancyWeighting(checkVectors, apiUsageDir)
    checkVectors = relevancyWeighting(checkVectors, waterOnlyDir) 
    ranking = scoresFromCheckVectors(checkVectors.d)    
       
    ranking.sort(reverse=True)
    
    """
    ranking = []    
    for (functionLocation, symbols) in WFuncs.d.iteritems():
        # number of _distinct_ symbols
        nSymbols = numpy.sum([1 for v in symbols.itervalues()])

        if not functionLocation in CFuncs.d:
            CFunc = []
        else:
            CFunc = CFuncs.d[functionLocation]
        
        score = 0.0
        for (s,occurrences) in symbols.iteritems():
            
            # This performs the projection onto the subspace
            if not s in F:
                # This is not a symbol ever used in a check
                continue
            
            occurrences = 1
            score += occurrences * F[s]
        
            if s in CFunc:
                # symbol occurs in check
                o = CFunc[s]
                o = 1
                score -= alpha*(o * F[s])
        score /= nSymbols
        ranking.append((score, functionLocation))
    
    ranking.sort(reverse=True)
    
    # Min-Max normalization of check-scores
    checkScoreMax = numpy.max([r[0] for r in ranking])
    checkScoreMin = numpy.min([r[0] for r in ranking])
    ranking = [ ((r[0]- checkScoreMin)/(checkScoreMax - checkScoreMin),r[1]) for r in ranking]
    
    
    termDocMatrix = pickle.load(file(waterOnlyDir + 'termDocMatrix.pickl'))
    functionLocations = termDocMatrix.index2Doc
    
    anomalyRanker = Ranker(waterOnlyDir)
    anomalyRanker.loadDistanceMatrix()
    anomalyScores = anomalyRanker.determineAnomaliesFromDistanceMatrix('gamma', 10)
    
    # Min-Max normalization of anomaly-scores
    anomalyScoresMax = numpy.max(anomalyScores)
    anomalyScoresMin = numpy.min(anomalyScores)
    anomalyScores = [(float(x) - anomalyScoresMin)/(anomalyScoresMax - anomalyScoresMin) for x in anomalyScores]
    
    anomalyTuples = zip(anomalyScores, functionLocations)
    anomalyDict = {}
    for (score, location) in anomalyTuples:
        anomalyDict[location] = score
    
    beta = 0.15
    combinedRanking = []
    for (score, functionLocation) in ranking:
        newScore = score
        if anomalyDict.has_key(functionLocation):
            anomalyScore = anomalyDict[functionLocation]
            
            newScore = beta*score + (1-beta)*anomalyScore
            
        combinedRanking.append((newScore, functionLocation))
    """
    
    ranking = [RankingEntry(r[0], r[1]) for r in ranking]
    pickle.dump(ranking, file(projectRoot + '../attackSurfaceRanking.pickl', 'w'))    

            
        
if __name__ == '__main__':
    import sys
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    main(projectRoot)