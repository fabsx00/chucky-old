
import pickle, os, sys

datasetDir = sys.argv[1]
if datasetDir[-1] != '/': datasetDir += '/'
JOERN_DIR = '../'

sourceDir = os.getcwd() + '/' + datasetDir
os.chdir(JOERN_DIR)

nDatapoints = max([int(x) for x in os.listdir(sourceDir + '/withCheck')])

for i in xrange(1,nDatapoints + 1):
    
    rankingFilename = '%s/combinations/%d/gammaCRanking.pickl' % (sourceDir, i)
    ranking = pickle.load(file(rankingFilename))
    ranking = [(r.score, r.position) for r in ranking]
    
    print '--- %d ---' % (i)
    for r in ranking: print r
