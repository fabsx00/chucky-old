import os, csv, sys

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

JOERN_DIR = '/home/fabs/git/joern/'

kmin = 1
kmax = 31

# for tau in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:

tau = 2.0


# ks = [6, 16, 21, 51, 11, 26, 31, 36]
ks = range(104, 1014, 10)

for kmax in ks:
# for tau in [1.0, 2.0]:

    for datasetDir in ['./libtiff4NoChange/', './firefox3/', './pidgin2.7.3/', './linuxNoChange/', './libpng/']:

        EXP_DIR = os.getcwd() + '/' + datasetDir
        COMBINATIONS_DIR = EXP_DIR + 'combinations/'
        symbolsOfInterest = shellquote(file(EXP_DIR + '/symbolOfInterest').readline()[:-1])
        

        nDatapoints = max([int(x) for x in os.listdir(EXP_DIR + '/withCheck')])
        for i in xrange(1, nDatapoints + 1):
            sourceDir = COMBINATIONS_DIR + str(i) + '/'

            oldDir = os.getcwd()
            os.chdir(JOERN_DIR)
            cmd = "ipython2 ./tools/MissingCheckRanker.py %s %d %d %f %s" % (sourceDir, kmin, kmax, tau, symbolsOfInterest)
            print cmd
            os.system(cmd)
            os.chdir(oldDir)

    DEST_DIR = '../results/%d_%d_%f_TFIDF/' % (kmin, kmax, tau)
    os.mkdir(DEST_DIR)
    cmd = 'bash copyResults.sh %s' % (DEST_DIR)
    print cmd
    os.system(cmd)
