
from libjoern.pythonast.PythonASTProcessor import PythonASTProcessor
from libjoern.ASTNodeTypes import FUNCTION_DEF
    
class FunctionASTIterator(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
        
        self.handlers[FUNCTION_DEF] = self.handleFunction
    
    """ Override this function """
    def handler(self, node):
        return False
            
    def handleFunction(self, node):
        self._setFunctionRow(node)
        return self.handler(node)

    def _setFunctionRow(self, node):
        self.functionRow = node.row


class LeafIterator(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
    
    """ Override this function """
    def leafHandler(self, node):
        pass
     
    def defaultHandler(self, node):
        if node.children == []:
            self.leafHandler(node)
        return True # continue expanding children