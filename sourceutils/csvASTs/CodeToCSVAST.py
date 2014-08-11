import subprocess
import os

AST_FILENAME = 'ast.csv'

class CodeToCSVAST:
    
    def __init__(self):
        self.codeSensorLocation = None
    
    def run(self, filename, dirForSourceFile):
        self._runCodeSensorOnFile(filename, dirForSourceFile)
    
    def _runCodeSensorOnFile(self, filename, dirForSourceFile):
        
        if not self.codeSensorLocation:
            self.codeSensorLocation = '/'.join(__file__.split('/')[:-1]) + '/' + 'CodeSensor.jar'
        outputFilename = dirForSourceFile + '/' + AST_FILENAME 
        
        os.system('java -jar %s %s > %s' % (self.codeSensorLocation, filename, outputFilename))
        
        """
        proc = subprocess.Popen( ['java', '-jar', self.codeSensorLocation,
                                 '%s > %s' % (filename, outputFilename)],
                               stdout=subprocess.PIPE)

        # save
        
        f = open(outputFilename, 'w')

        while 1:
            line = proc.stdout.readline()
            f.write(line)
            if line == '': break
        f.close()
        """
