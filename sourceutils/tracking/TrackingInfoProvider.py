
import os
import cPickle as pickle

from sourceutils.tracking.TrackingInformationGenerator import TrackingInformationGenerator

class TrackingInfoProvider:
    def __init__(self):
        self.trackingInfoGenerator = TrackingInformationGenerator()
        self.cachedTrackingInfos = {}
    
    def loadTrackingInfo(self, location):
        filename = location + '/tracking_info.pickl'
        
        if not os.path.exists(filename):
            self._createTrackingInfo(location)
        
        if filename in self.cachedTrackingInfos:
            return self.cachedTrackingInfos[filename]
        self.cachedTrackingInfos[filename] = pickle.load(file(filename))
        return self.cachedTrackingInfos[filename]
    
    def _createTrackingInfo(self, location):
        self.trackingInfoGenerator.reset(location)
        self.trackingInfoGenerator.process()
        self.trackingInfoGenerator.save()