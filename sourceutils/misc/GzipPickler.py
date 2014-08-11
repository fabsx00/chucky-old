import cPickle as pickle
import gzip

class GzipPickler:
    
    def dump(self, obj, filename):
        # f = gzip.GzipFile(filename, 'wb')
        f = file(filename, 'w')
        pickle.dump(obj, f, protocol=2)
        f.close()

    def load(self, filename):
        # f = gzip.GzipFile(filename, 'rb')
        f = file(filename)
        obj = pickle.load(f)
        f.close()
        return obj
