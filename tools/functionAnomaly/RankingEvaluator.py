
import pickle, numpy
from LabelLoader import LabelLoader

class RankingEvaluator:

    def __init__(self, datasetDir, labelFilename = 'labels.txt'):
        self.datasetDir = datasetDir
        self.labelLoader = LabelLoader(labelFilename)
        
        self.determineProjects()
   
    def generateAverageCDF(self, rankingName, reverse = False, constantLengthDict=False):
        
        self.reverse = reverse
        averageCdf = None
        
        for p in self.projects:
            (ranking, vulnerableEntries) = self.getRankingAndVulnsForProject(p, rankingName)
            self.printVulnerableEntries(p, vulnerableEntries)
            lengthDict = self.generateLengthDictForProject(p, constantLengthDict)
            (X,Y) = self.generateCDF(ranking, vulnerableEntries, lengthDict)
            print X
            (X, cdf) = self.interpolate(X, Y)
            if averageCdf == None:
                averageCdf = cdf
            else:
                averageCdf += cdf
        
        averageCdf /= len(self.projects)
        return (X, averageCdf)
    
    def generateHistograms(self, rankingName, reverse=False):
        self.reverse = reverse
        
        for p in self.projects:
            self.generateHistogramsForProject(p, rankingName)
    
    def generateHistogramsForProject(self, project, rankingName):
        (ranking, vulnerableEntries) = self.getRankingAndVulnsForProject(project, rankingName)
        scores = self.getScoresFromRanking(ranking)
        vulnScores = self.getScoresFromRanking(vulnerableEntries)
        
        
        minVulnScore = numpy.min(vulnScores)
        maxVulnScore = numpy.max(vulnScores)
        
        print 'MinVulnScore: %f' % (minVulnScore)
        print 'MaxVulnScore: %f' % (maxVulnScore)
        print 'nInBand: %f' % (len([s for s in scores if s >= minVulnScore and s <= maxVulnScore]))
        print 'nOutOfBand: %f' % (len([s for s in scores if s < minVulnScore or s > maxVulnScore]))
        
        
        import pylab
        pylab.figure()
        pylab.hist(scores, 1000)
        pylab.figure()
        pylab.hist(vulnScores, 1000)
    
        for r in ranking:
            print r
    
    def getScoresFromRanking(self, ranking):
        return [r.score for r in ranking]
        
      
    def printVulnerableEntries(self, projectName, vulnerableEntries):
        print projectName
        for entry in vulnerableEntries: print entry
        
    
           
    def generateGlobalCDF(self, rankingName, reverse = False, constantLengthDict = False):
        self.reverse = reverse
        
        (globalRanking, vulnerableEntries) = self.generateGlobalRanking(rankingName)
        globalLengthDict = self.generateGlobalLengthDict(constantLengthDict)
        
        (X,Y) = self.generateCDF(globalRanking, vulnerableEntries, globalLengthDict)
        return (X, Y)
    
    def generateGlobalRanking(self, rankingName):
        
        vulnerableEntries = []
        globalRanking = []

        for p in self.projects:
            (projectRanking, projectVulns) = self.getRankingAndVulnsForProject(p, rankingName)
            globalRanking.extend(projectRanking)
            vulnerableEntries.extend(projectVulns)
       
        globalRanking.sort()
        vulnerableEntries.sort()
        return (globalRanking, vulnerableEntries)
    
        
    def determineProjects(self):
                
        projectIndexFilename = self.getProjectIndexFilename()
                
        lines = file(projectIndexFilename).readlines()
        self.projects = [l.replace('\n', '') for l in lines]
        
        print self.projects

    def getProjectIndexFilename(self):
        return self.datasetDir + 'cleanedup'

    def getRankingAndVulnsForProject(self, projectName, rankingName):
        projectRanking = self.getRankingForProject(projectName, rankingName)    
        vulnerableEntries = self.getVulnerableEntriesForProject(projectName, projectRanking)
        return (projectRanking, vulnerableEntries)

    def getRankingForProject(self, project, rankingName):
        
        rankingFilename = self.datasetDir + project + '/%s' % (rankingName)
        ranking = pickle.load(file(rankingFilename))
        if self.reverse:
                for r in ranking: r.invert()
        ranking.sort()
        return ranking

    def getVulnerableEntriesForProject(self, project, projectRanking):
        self.labelLoader.loadLabels(project, self.datasetDir)
        vulnerableEntries = self.labelLoader.getPositionsOfVulns(projectRanking)
        return vulnerableEntries

    def generateGlobalLengthDict(self, constantLengthDict):
        lengthDict = {}
        
        for p in self.projects:
            projectLengthDict = self.generateLengthDictForProject(p, constantLengthDict)
            lengthDict.update(projectLengthDict)
        return lengthDict
        
        
    def generateLengthDictForProject(self, projectName, constantLengthDict):
        if constantLengthDict:
            return self.generateConstantLengthDictForProject(projectName)
        
        functionIndex = pickle.load(file(self.datasetDir + projectName + '/parsed/functionIndex.pickl'))
        d = {} 
        for (unused,functionLocations) in functionIndex.d.iteritems():
            for (row, location) in functionLocations:
                if d.has_key(location): print 'WARN'
                d[location] = self.functionLengthFromRow(row)
        return d

    def generateConstantLengthDictForProject(self, projectName):        
        functionIndex = pickle.load(file(self.datasetDir + projectName + '/parsed/functionIndex.pickl'))
        d = {} 
        for (unused,functionLocations) in functionIndex.d.iteritems():
            for (row, location) in functionLocations:
                if d.has_key(location): print 'WARN'
                d[location] = 1
        return d


    def functionLengthFromRow(self, row):
        (startLine, startPos) = row[1].split(':') #@UnusedVariable
        (endLine, endPos) = row[2].split(':') #@UnusedVariable
        length = int(endLine) - int(startLine) + 1
        return length

    def rankingEntryToLocation(self, rankingEntry):
        (filename, funcName, pos) =  rankingEntry.position
        (line, col) = pos.split(':')
        return 'sourceDir/%s/%s_%s_%s' % (filename, funcName, line, col)

    def generateCDF(self, ranking, vulnerableEntries, lengthDict):
        nVulns = len(vulnerableEntries)
        totalLinesOfCode = sum(lengthDict.values())
        
        X = [0]
        Y = [0]

        nFound = 0

        positions = vulnerableEntries[:]
        converter = self.rankingEntryToLocation

        for i in xrange(len(ranking)):
            
            if len(positions) == 0:
                continue

            if positions[0] == ranking[i]:
                positions.pop(0)
                nFound += 1
                readFunctionLinesOfCode = [lengthDict[converter(r)] for r in ranking[:i]]
                linesOfCodeRead = numpy.sum(readFunctionLinesOfCode)
                
                X.append( 100 * float(linesOfCodeRead) / totalLinesOfCode)
                Y.append( 100 * float(nFound)/ nVulns)
        X.append(100)
        Y.append(100)
        return (X,Y)

    def interpolate(self, X,Y):
        xvals = numpy.linspace(0,100,100)
        return (xvals, numpy.interp(xvals, X, Y))
