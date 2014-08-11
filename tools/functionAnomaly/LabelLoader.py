
class LabelLoader:
    
    def __init__(self, labelsFilename = 'labels.txt'):
        self.labelsFilename = labelsFilename
    
    def loadLabels(self, project, datasetDir):

        labelsFilename = datasetDir + project + '/%s' % (self.labelsFilename)
        f = file(labelsFilename)
        self.labels = [self._loadLabelLine(line) for line in f.readlines()]
        f.close()
    
    def _loadLabelLine(self, line):
        x = line.split(' ')
        return (x[0], x[1], x[2][:-1])

    def getPositionsOfVulns(self, ranking):
        return [r for r in ranking if self.vulnMatches(r)]

    def vulnMatches(self, rankRow):
        rankRowVulnLocation =(rankRow.position[0], rankRow.position[1], rankRow.position[2])
        return rankRowVulnLocation in self.labels