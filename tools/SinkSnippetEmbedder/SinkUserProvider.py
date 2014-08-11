
import cPickle as pickle

class SinkUserProvider:
    def __init__(self, projectRoot):
        self._setProjectRoot(projectRoot)
        self._loadCallIndex()
    
    def _setProjectRoot(self, projectRoot):
        self.projectRoot = projectRoot
        if self.projectRoot[-1] != '/': self.projectRoot += '/'
    
    def _loadCallIndex(self):
        filename = self.projectRoot + 'callIndex.pickl'
        self.callIndex = pickle.load(file(filename))

    def getSinkByName(self, name):
        return (name, self.callIndex.d[name])

    def getSinks(self, minCallsToSink = 0):
        d = self.callIndex.d
        return [item for item in d.iteritems() if len(item[1]) >= minCallsToSink]
    
    