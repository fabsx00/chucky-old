import sys, os

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

projectName = sys.argv[1]
if projectName[0] != '.': projectName = './' + projectName

symbolsOfInterest = shellquote(sys.argv[2])

cmd = 'rm -rf %s/combinations/' % (projectName)
os.system(cmd)

cmd = 'mkdir %s/combinations' % (projectName);
os.system(cmd)

nDatapoints = max([int(x) for x in os.listdir(projectName + '/withCheck')])

cmd = 'for i in `seq 1 %d`; do python2 ./generate.py $i %s/; done' % (nDatapoints, projectName)
os.system(cmd)

cmd = "ipython2 ./run.py %s %s;" % (projectName, symbolsOfInterest)
os.system(cmd)

# cmd = 'ipython2 ./eval.py %s' % (projectName) 
# os.system(cmd)
