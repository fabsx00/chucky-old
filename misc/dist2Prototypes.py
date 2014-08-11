
import sys, pickle
import numpy

thresh = 0.0001

projectRoot = sys.argv[1]
if projectRoot[-1] != '/': projectRoot += '/'

# termDocMatrixFilename = projectRoot + 'termDocMatrix.pickl'
# T = pickle.load(file(termDocMatrixFilename))
# M = T.matrix.tocsc().T
# labels = T.index2Doc

prototypeFilename = projectRoot + 'W.pickl'
W = pickle.load(file(prototypeFilename))

sinkMatrixFilename = projectRoot + 'sinkDocs.pickl'
S = pickle.load(file(sinkMatrixFilename))
M = S.tocsc().T
labelFilename = projectRoot + 'sinkLabels.pickl'
labels = pickle.load(file(labelFilename))


i = 0

for prototypeVec in W.T:

    I = prototypeVec > thresh
    D = numpy.abs(M - prototypeVec)
    D = numpy.multiply(D, I)
    D = D.sum(axis=1)
    dists = [(D[j][0,0], i, labels[j]) for j in range(len(D))]
    dists.sort()
    
    for d in dists:
        print  '%f, %d, %s' %  d

    i += 1