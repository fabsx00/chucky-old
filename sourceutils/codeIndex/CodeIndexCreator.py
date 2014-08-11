
from sourceutils.misc.NameToListMap import NameToListMap

from libjoern.csvast.CSVProcessor import CSVProcessor
from libjoern.ASTNodeTypes import FUNCTION_NAME, CALLEE


class CodeIndexCreator(CSVProcessor):
    def __init__(self, projectRoot):
        CSVProcessor.__init__(self)
        
        self.projectRoot = projectRoot
        if self.projectRoot[-1] != '/': self.projectRoot += '/'
        
        self.functionIndex = NameToListMap()
        self.callIndex = NameToListMap()
        self.declarationIndex = NameToListMap()
        self.conditionIndex = NameToListMap()
                
        self.handlers[FUNCTION_NAME] = self.functionHandler
        self.handlers[CALLEE] = self.callHandler
        # self.handlers['VAR_DECL'] = self.declHandler
        # self.handlers['cond'] = self.condHandler
    
    def registerFunction(self, row):
        funcDir = self.getDirForFilename(self.currentFile)
        functionName = row[4]
        self.currentFunctionName = functionName
        self.functionIndex.add((row, funcDir), functionName)
        
    def registerCall(self, row):
        funcDir = self.getDirForFilename(self.currentFile)
        callDstName = row[4]
        self.callIndex.add((row, funcDir), callDstName)
    
    def registerDecl(self, row):
        funcDir = self.getDirForFilename(self.currentFile)
        typeName = row[4]
        self.declarationIndex.add((row, funcDir), typeName)
    
    def registerCond(self, row):
        funcDir = self.getDirForFilename(self.currentFile)
        cond = row[4]
        self.conditionIndex.add((row, funcDir), cond)
    
    def functionHandler(self, row):
        self.registerFunction(row)
    
    def callHandler(self, row):
        self.registerCall(row)
        
    def declHandler(self, row):
        self.registerDecl(row)
    
    def condHandler(self, row):
        self.registerCond(row)
    
    def getDirForFilename(self, filename):
        retval = '/'.join(filename.split('/')[:-1])[len(self.projectRoot):]
        return retval
    
    def saveResults(self):
        
        outputDir = self.projectRoot
        self.functionIndex.save(outputDir + 'functionIndex.pickl')
        self.callIndex.save(outputDir + 'callIndex.pickl')
        self.declarationIndex.save(outputDir + 'declarationIndex.pickl')
        self.conditionIndex.save(outputDir + 'conditionIndex.pickl')
        
