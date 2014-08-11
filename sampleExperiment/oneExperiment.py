import os, sys

datasetDir = sys.argv[1]
if datasetDir[-1] != '/': datasetDir += '/'

symbolsOfInterest = sys.argv[3]

JOERN_DIR = '/home/fabs/git/joern/'
EXP_DIR = os.getcwd() + '/' + datasetDir
COMBINATIONS_DIR = EXP_DIR + 'combinations/'
CODE_CACHE_DIR = EXP_DIR + 'codeCache/'

os.chdir(JOERN_DIR)

i = int(sys.argv[2])
sourceDir = COMBINATIONS_DIR + str(i) + '/'
parsedDir = JOERN_DIR + '.%d/' % (i)

os.system('./joern_parse %s' % (sourceDir))

# If this is the first experiment, copy to code-cache
if not os.path.exists(CODE_CACHE_DIR):
    os.mkdir(CODE_CACHE_DIR)
    cmd = 'cp -r %ssourceDir/otherCode/ %s' % (parsedDir, CODE_CACHE_DIR)
    print 'copying to code cache: '
    print cmd
    os.system(cmd)
else:
    # This is not the first experiment. Link to codeCache.
    cmd = 'ln -s %sotherCode/ %ssourceDir/otherCode' % (CODE_CACHE_DIR, parsedDir)
    # cmd = 'cp -r %sotherCode/ %ssourceDir/' % (CODE_CACHE_DIR, parsedDir)
    print 'Copying FROM codeCache'
    print cmd
    os.system(cmd)

os.system('./joern_index %s' % (parsedDir))
os.system('mv %s %s/parsed/' % (parsedDir, sourceDir))
os.system('./tools/glitchFinder/glitchFinderEmbed.py --ngram-n 1 --tfidf --filter APISymbols %s' % (sourceDir + 'parsed/'))
os.system('./tools/glitchFinder/glitchFinderEmbed.py --ngram-n 1 --filter Symbols %s' % (sourceDir + 'parsed/'))
os.system('ipython2 ./mlutils/distanceMatrix/createFromTermDocMatrix.py %s/embeddings/APISymbols_1.pickl/ cosine' % (sourceDir + 'parsed/'))

# os.system('ipython2 ./sourceutils/tracking/create.py %s' % (sourceDir + 'parsed'))
# os.system('ipython2 ./sourceutils/expressionTrees/create.py %s' % (sourceDir + 'parsed'))
# os.system('ipython2 ./tools/functionLengthRanker.py %s' % (sourceDir))
kmin = 1
kmax = 21
tau = 2.0
cmd = "ipython2 ./tools/MissingCheckRanker.py %s %d %d %f '%s'" % (sourceDir, kmin, kmax, tau, symbolsOfInterest)
print cmd
os.system(cmd)
