from ConditionalAnomalyCalculator import ConditionalAnomalyCalculator
from FunctionContextProvider import FunctionContextProvider

KMIN = 1
KMAX= 21
TAU = 0.92
        
def outputSummary(contextsForFunction, location):
    
    contexts = [(len(context.neighbours), context.gammaC, symbol, context) for (symbol, context) in contextsForFunction.iteritems()]
    contexts.sort()
    
    for (nNeighbours, gammaC, symbol, context) in contexts:
        print 'Symbol: %s: Support: %d, Score: %f' % (symbol, nNeighbours, gammaC)
        context.printNeighbourhood()
        context.printModel()
        context.printDeviation()
    
def main(projectRoot, functionLocation, kmin=KMIN, kmax=KMAX, tau=TAU, symbolsOfInterest=None):
    
    contextProvider = FunctionContextProvider(projectRoot)
    contextProvider.configure(kmin, kmax, tau, symbolsOfInterest)
    
    contextsForFunction = contextProvider.getContextsForFunction(functionLocation)
    
    anomalyCalculator = ConditionalAnomalyCalculator()
    anomalyCalculator.conditionalAnomaly(contextsForFunction)    
    
    outputSummary(contextsForFunction, functionLocation)
    return contextsForFunction
            
if __name__ == '__main__':
    import sys, ast
    projectRoot = sys.argv[1]
    if projectRoot[-1] != '/': projectRoot += '/'
    functionLocation = sys.argv[2]
    print functionLocation
    
    symbolsOfInterest = None
    kmin = KMIN
    kmax = KMAX
    tau = TAU
    
    try:
        kmin = sys.argv[3]
        kmax = sys.argv[4]
        tau = sys.argv[5]
        symbolsOfInterest = sys.argv[6]        
    except:
        pass
    
    if symbolsOfInterest:
        symbolsOfInterest = ast.literal_eval(symbolsOfInterest)
        symbolsOfInterest = [str(x) for x in symbolsOfInterest]

    main(projectRoot, functionLocation, kmin, kmax, tau, symbolsOfInterest)
    
