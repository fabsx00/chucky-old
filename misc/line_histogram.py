
import sys
import operator

f = file(sys.argv[1])

d = dict()

for line in f.readlines():
    try:
        d[line] += 1
    except:
        d[line] = 1
f.close()

sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
for item in sorted_d: print item
