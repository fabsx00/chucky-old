import sys, pickle, os
import numpy as np
import re
    
epsilon = 0.000000001

def normalize(cluster):
    if cluster == []: return []
    scores = [m[0] for m in cluster]
    minScore = np.min(scores)
    maxScore = np.max(scores)
    
    
    return [ (float(m[0] - minScore) / (maxScore - minScore + epsilon),) + m[1:] for m in cluster]

def maxRanking(ranking):
    ranking = toFunctionNameRanking(ranking)
    ranking = keepOnlyMaxRanked(ranking)
    ranking = [(0, r) for r in ranking]
    return ranking

def averageRanking(ranking):
    
    return [(r[0], functionNameFromRow(r[3])) for r in ranking]
    
    d = {}
    
    for r in ranking:
        score = r[0]
        funcName = functionNameFromRow(r[3])
        if d.has_key(str(funcName)):
            d[str(funcName)][1].append(score)
        else:
            d[str(funcName)] = (funcName, [score])
    
    newRanking = []
    for (k,scores) in d.iteritems():
        avgScore = float(np.sum(scores[1])) / len(scores[1])
        funcName = scores[0]
        newRanking.append((avgScore, funcName))
    
    newRanking.sort(reverse=True)
    return newRanking

def sumRanking(ranking):
    
    d = {}
    
    for r in ranking:
        score = r[0]
        funcName = functionNameFromRow(r[3])
        if d.has_key(str(funcName)):
            d[str(funcName)][1].append(score)
        else:
            d[str(funcName)] = (funcName, [score])
    
    newRanking = []
    for (k,scores) in d.iteritems():
        sumScore = float(np.sum(scores[1]))
        funcName = scores[0]
        newRanking.append((sumScore, funcName))
    
    newRanking.sort(reverse=True)
    return newRanking
    


def toFunctionNameRanking(ranking):
    return [functionNameFromRow(r[3]) for r in ranking]
    
def functionNameFromRow(r):
    x = r.split('/')
    sourceFilename = ('/'.join(x[:-1]))
    i = sourceFilename.find('sourceDir/')
    sourceFilename = sourceFilename[i+len('sourceDir/'):]
    funcName = x[-1] #[:-2]
    match = re.search('(.*?)_(\d+)_(\d+)$', funcName)
    funcName = match.group(1)
    pos = str(match.group(2)) + ':' + str(match.group(3))
    return [sourceFilename, funcName, pos]

def keepOnlyMaxRanked(ranking):
    d = {}
    newRanking = []

    for r in ranking:
        if not d.has_key(str(r)):
            newRanking.append(r)
            d[str(r)] = 1
    return newRanking

    
def main(projectRoot):
    
    clusterDir = projectRoot + 'clusters/'
    
    globalCallRanking = []
    
    for filename in os.listdir(clusterDir):
        if filename == 'README': continue
        
        clusters = pickle.load(file(clusterDir + filename))
        
        for cluster in clusters:
            cluster = normalize(cluster)
            for member in cluster:
                globalCallRanking.append(member)
    
    if globalCallRanking != []:
    
        globalCallRanking.sort(reverse=True)
        avgRanking = averageRanking(globalCallRanking)
        maxRanking_ = maxRanking(globalCallRanking)
        sumRanking_ = sumRanking(globalCallRanking)
    
        pickle.dump(globalCallRanking, file(projectRoot + 'ranking.pickl', 'w'))
        pickle.dump(avgRanking, file(projectRoot + 'averageRanking.pickl', 'w'))
        pickle.dump(maxRanking_, file(projectRoot + 'maxRanking.pickl', 'w'))
        pickle.dump(sumRanking_, file(projectRoot + 'sumRanking.pickl', 'w'))
    else:
        print 'Warning: Global ranking empty. Method has probably not been run'
    
    
if __name__ == '__main__':
    
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    
    main(projectRoot)