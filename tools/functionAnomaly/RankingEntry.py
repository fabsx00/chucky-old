import re


class RankingEntry:
    def __init__(self, score, location, doConversion = True):
        self.score = score
        if doConversion:
            self.position = self.rankingPositionFromLocation(location)
        else:
            self.position = location

    def rankingPositionFromLocation(self, location):
        x = location.split('/')
        sourceFileName = '/'.join(x[:-1])   
        i = sourceFileName.find('sourceDir/')
        sourceFileName = sourceFileName[i+len('sourceDir/'):]    
        y = x[-1].split('_')
        funcName = '_'.join(y[:-2]) 
        pos = ':'.join(y[-2:])
        match = re.search('(\d+):(\d+)', pos)
        pos = match.group(1) + ':' + match.group(2)
        return [sourceFileName, funcName, pos]
    
    def invert(self):
        self.score = -self.score

    def __str__(self):
        return str((self.score, self.position))

    def __lt__(self, other):
        return self.score < other.score
    