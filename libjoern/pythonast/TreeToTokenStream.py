import cStringIO as StringIO
from libjoern.pythonast.PythonASTProcessor import PythonASTProcessor

class TreeToTokenStream(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
    
    def reset(self):
        pass
        
    def apply(self, node):
        self.s = StringIO.StringIO()
        self.processTree(node)
        self.s.seek(0)
        lines = self.s.readlines()
        self.s = None
        # cut off newline
        return [l[:-1] for l in lines]
              
    def defaultHandler(self, node):
        # By default, traverse children
        return True
