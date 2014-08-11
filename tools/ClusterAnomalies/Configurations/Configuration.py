

THRESH = 2

# Embedding parameters
    
DEFAULT_NGRAM_N  = 3
DEFAULT_SMALLER_NGRAMS_TOO = True
    
# NMF/SVD parameters
    
DEFAULT_MIN_NUM_MEMBERS  = 2
DEFAULT_IN_ACCEPTABLE = 1
DEFAULT_ALGORITHM = 'SVD'

class Configuration:
    def __init__(self):
        self.c = {}
        self.c['ngramN'] = DEFAULT_NGRAM_N
        self.c['smallerNgramsToo'] = DEFAULT_SMALLER_NGRAMS_TOO
        self.c['minimumNumMembers'] = DEFAULT_MIN_NUM_MEMBERS
        self.c['inAcceptable'] = DEFAULT_IN_ACCEPTABLE
        self.c['algorithm'] = DEFAULT_ALGORITHM
    
    def __getitem__(self, key):
        return self.c[key]
    
    def output(self):
        pass