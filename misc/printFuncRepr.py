import sys, pickle

f = pickle.load(file(sys.argv[1]))

funcs = f.d.keys()

for func in sorted(funcs):
    print 'name: ' + func
    print '================'
    
    for (k,v) in f.d[func].iteritems():
        print (k,v)
    
