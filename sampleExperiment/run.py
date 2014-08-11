import os, sys

datasetDir = sys.argv[1]
if datasetDir[-1] != '/': datasetDir += '/'

symbolsOfInterest = sys.argv[2]

JOERN_DIR = '../'
EXP_DIR = os.getcwd() + '/' + datasetDir
COMBINATIONS_DIR = EXP_DIR + 'combinations/'
CODE_CACHE_DIR = EXP_DIR + 'codeCache/'


# Remove old code-cache
# if os.path.exists(CODE_CACHE_DIR):
#    cmd = 'rm -rf %s' % (CODE_CACHE_DIR)
#    os.system(cmd)

nDatapoints = max([int(x) for x in os.listdir(EXP_DIR + '/withCheck')])

for i in xrange(1,nDatapoints + 1):
    cmd = "python2 ./oneExperiment.py %s %d '%s'" % (datasetDir,i,symbolsOfInterest)
    print cmd
    os.system(cmd)
