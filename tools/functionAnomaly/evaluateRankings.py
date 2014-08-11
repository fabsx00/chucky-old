
from RankingEvaluator import RankingEvaluator
import pylab

datasetDir = '/mnt/smbshare/projects/offsec/anomaly/debianDataset/'
    
    
def plotCDFs(labelsFilename): 
    legend = []
    
    constantLengthDict = False

    pylab.hold(True)
    
    # plotGammaAndZeta(constantLengthDict, legend, labelsFilename)
    
    evaluator = RankingEvaluator(datasetDir)
  
    
    (X,Y) = evaluator.generateAverageCDF('lengthRanking.pickl', reverse = True, constantLengthDict=constantLengthDict)
    # (X,Y) = evaluator.generateGlobalCDF('lengthRanking.pickl', reverse = True, constantLengthDict=constantLengthDict)
    pylab.plot(X, Y)
    legend.append('len')
  
    evaluator = RankingEvaluator(datasetDir)    
    (X,Y) = evaluator.generateAverageCDF('gammaCRanking.pickl', reverse = True, constantLengthDict=constantLengthDict)
    # (X,Y) = evaluator.generateGlobalCDF('gammaCRanking.pickl', reverse = True, constantLengthDict=constantLengthDict)
    pylab.plot(X, Y)
    legend.append('gammaC')
    
    pylab.plot([0, 100], [0,100])
    legend.append('rand')
    
    pylab.legend(legend)
    pylab.xlabel('Percentage of the code base read')
    pylab.ylabel('Percentage of vulnerabilities found')
    
    
    # evaluator.generateHistograms('attackSurfaceRanking.pickl')
    
    
def plotGammaAndZeta(constantLengthDict, legend, labelsFilename):
    
    for anomalyScore in ['gamma', 'zeta']:
        for k in [10, 22, 30, 50]:
            legend.append('%s, k=%d' % (anomalyScore, k))
            
            evaluator = RankingEvaluator(datasetDir, labelsFilename)
            rankingName = 'termDocMatrixRanker_%s_%d.pickl' % (anomalyScore, k)
            
            # (X, Y) = evaluator.generateGlobalCDF(rankingName)
            (X, Y) = evaluator.generateAverageCDF(rankingName, constantLengthDict=constantLengthDict)
            
            pylab.plot(X, Y)
            pylab.hold(True)
    


def plotHistograms(labelsFilename):
    
    for anomalyScore in ['gamma', 'zeta']:
        for k in [10, 22, 30, 50]:
            evaluator = RankingEvaluator(datasetDir, labelsFilename)
            rankingName = 'termDocMatrixRanker_%s_%d.pickl' % (anomalyScore, k)
            evaluator.generateHistograms(rankingName)
    
def main(labelsFilename):
    plotCDFs(labelsFilename)
    # plotHistograms(labelsFilename)    
    pylab.show()



if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        labels = sys.argv[1]
    else:
        labels = 'labels.txt'
    
    main(labels)
