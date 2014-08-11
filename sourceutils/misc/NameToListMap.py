import cPickle as pickle

class NameToListMap():
    def __init__(self):
        self.d = dict()
    
    def add(self, itemToAdd, name):
        try:
            self.d[name].append(itemToAdd)
        except:
            self.d[name] = [itemToAdd]

    def save(self, filename):
        pickle.dump(self, open(filename, 'wb'), protocol=2)
    