import os, re

SOURCE_FILE_AST_FILENAME = 'ast\.(csv)$'
SOURCE_FILE_PYTHON_AST_FILENAME = 'ast\.pickl$'

FUNCTION_AST_FILENAME = 'func_ast\.(csv)$'
FUNCTION_PYTHON_AST_FILENAME = 'func_ast\.pickl$'

""" Base class for all FileIterators """

class FileIterator:
  
    def __init__(self, projectRoot):
        self.projectRoot = projectRoot
        self.filterRegex = ''
    
    def setFilenameFilterRegex(self, r):
        self.filterRegex = re.compile(r)
        
    def __iter__(self):
        for (dirpath, unused_dirnames, filenames) in os.walk(self.projectRoot, followlinks=True):
            for name in filenames:
                if not self.isOfInterest(name): continue
                absoluteName = dirpath + '/' + name
                yield absoluteName
        
    def getDirForFilename(self, filename):
        return '/'.join(filename.split('/')[:-1])

    def isOfInterest(self, filename):
        return self.filterRegex.match(filename)


class SourceFileWalker(FileIterator):
    def __init__(self, projectRoot):
        FileIterator.__init__(self, projectRoot)
        self.setFilenameFilterRegex('source$')

class SourceFileASTIterator(FileIterator):
    def __init__(self, projectRoot):
        FileIterator.__init__(self, projectRoot)
        self.setFilenameFilterRegex(SOURCE_FILE_AST_FILENAME)

class SourceFilePythonASTIterator(FileIterator):
    def __init__(self, projectRoot):
        FileIterator.__init__(self, projectRoot)
        self.setFilenameFilterRegex(SOURCE_FILE_PYTHON_AST_FILENAME)

class FunctionASTIterator(FileIterator):
    def __init__(self, projectRoot):
        FileIterator.__init__(self, projectRoot)
        self.setFilenameFilterRegex(FUNCTION_AST_FILENAME)

class FunctionPythonASTIterator(FileIterator):
    def __init__(self, projectRoot):
        FileIterator.__init__(self, projectRoot)
        self.setFilenameFilterRegex(FUNCTION_PYTHON_AST_FILENAME)
