import cPickle as pickle


class FunctionIndex:
    def __init__(self, projectRoot):
        self.projectRoot = projectRoot
        self._load()
    
    def getFunctionNameIterator(self):
        return self.index.d.iterkeys()
    
    def getLocationIterator(self):
        return self._locationIterator()
    
    def _locationIterator(self):
        for locations in self.index.d.itervalues():
            for (row, location) in locations: #@UnusedVariable
                yield location
        
    def _load(self):
        indexFilename = self.projectRoot + '/functionIndex.pickl'
        self.index = pickle.load(file(indexFilename))
    
