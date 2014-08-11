
from tools.functionAnomaly.RankingEntry import RankingEntry

import sys, pickle

def functionLengthFromRow(row):
    (startLine, startPos) = row[1].split(':') #@UnusedVariable
    (endLine, endPos) = row[2].split(':') #@UnusedVariable
    length = int(endLine) - int(startLine)
    return length

def locationToRankingName(location):
    return '/'.join(location.split('/')[:-1])[len('sourceDir/'):]
    

projectRoot = sys.argv[1]
if projectRoot[-1] != '/': projectRoot += '/'

ranking = []

functionIndex = pickle.load(file(projectRoot + 'parsed/functionIndex.pickl'))
for (functionName,functionLocations) in functionIndex.d.iteritems():
    for (row, location) in functionLocations:
        funcLen = functionLengthFromRow(row)
        ranking.append(RankingEntry(funcLen, location))
        

ranking.sort(reverse=True)
pickle.dump(ranking, file(projectRoot + 'lengthRanking.pickl', 'w'))
