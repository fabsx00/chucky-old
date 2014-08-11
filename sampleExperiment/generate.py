import sys, os

n = sys.argv[1]
datasetDir = sys.argv[2]
if datasetDir[-1] != '/': datasetDir += '/'
withCheckDir = datasetDir + 'withCheck/'
withoutCheckDir = datasetDir + 'withoutCheck/'
outDir = datasetDir + 'combinations/'
otherCodeDir = datasetDir + 'otherCode/'

CODE_CACHE_DIR = datasetDir + 'codeCache/'

try:
    os.mkdir(outDir)
except:
    pass

noCheckFunc = file(withoutCheckDir + n).readlines()

outDir += n + '/'
try:
    os.mkdir(outDir)
except:
    pass


outDir +=  'sourceDir/'
os.mkdir(outDir)

outFilename = outDir + 't.c'

outFile = file(outFilename, 'w')
outFile.writelines(noCheckFunc)
outFile.write('\n');

nDatapoints = max([int(x) for x in os.listdir(datasetDir + '/withCheck')])

for i in xrange(1, nDatapoints + 1):
    if i == int(n):
        continue
    checkFunc = file(withCheckDir + str(i)).readlines()
    outFile.writelines(checkFunc)
    outFile.write('\n');

outFile.close()

if n == '1' and not os.path.exists(CODE_CACHE_DIR):
    os.system('cp -r %s %s' % (otherCodeDir, outDir))
