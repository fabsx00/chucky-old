#!/usr/bin/env python2

import pickle, sys


def calledMostOften(projectRoot, outputToStdout = False):
    
    retList = []
    
    callIndex = pickle.load(file(projectRoot + 'callIndex.pickl'))
    callDict = callIndex.d
    nCallsToSink = [(len(sources),sink) for (sink,sources) in callDict.iteritems()]
    nCallsToSink.sort(reverse=True)

    for c in nCallsToSink:
        if outputToStdout:
            print c[1]
        retList.append(c[1])
    
    return retList
    
if __name__ == '__main__':
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    calledMostOften(projectRoot, True)