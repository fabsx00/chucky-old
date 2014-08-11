import numpy as np
import matplotlib.pyplot as plt
import pickle


T = pickle.load(file('.toyProblem/termDocMatrix.pickl'))

data = np.array(pickle.load(file('H.pickl')).T)
labels = [t.split('/')[-1] for t in T.index2Doc]


print 'Number of datapoints: %d' % (data.shape[0])
print 'Number of dimensions: %d' % (data.shape[1])
print 'Number of labels: %d' % (len(labels))


# plt.subplots_adjust(bottom = 0.1)

X = data[:, 0]
Y = data[:, 1]
print X
print Y

plt.scatter(X , Y, marker = 'o')

for label, x, y in zip(labels, X, Y):
    plt.annotate( label, xy = (x,y)
        #, ha = 'right', va = 'bottom',
        #bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        )

    print '%f,%f: %s' % (x,y,label)

plt.show()
