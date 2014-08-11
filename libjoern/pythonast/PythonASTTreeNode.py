from libjoern.csvast.CSVRowAccessors import getCSVRowType


class PythonASTTreeNode():
    def __init__(self, row):
        self.row = row
        self.children = []
        self.parent = None
        
    def getType(self):
        return getCSVRowType(self.row)
    
    def hasNoChildren(self):
        return self.children == []

    def appendChild(self, child):
        self.children.append(child)

    def applyFunc(self, f):
        self.row = f(self.row)
        for child in self.children:
            child.applyFunc(f)
    
    def copyOnlyNode(self):
        newNode = PythonASTTreeNode(self.row[:])
        return newNode
      
    def __str__(self):
        childStrings = [str(child) for child in self.children]
        return '@+\%s%s+@' % (str(self.row), ''.join(childStrings))
    
    def toCSV(self):
        
        # This is a bottleneck.
        
        csvRow = '%s\n' % ('\t'.join(self.row))
        childStrings = [child.toCSV() for child in self.children]
        return '%s%s' % (csvRow, ''.join(childStrings)) 
        
    def searchNodeByRow(self, row):
        queryRow = row[:4]
        return self._searchNodeByRow(queryRow)
    
    def _searchNodeByRow(self, row):
         
        if self.row[:4] == row:
            return self
        
        for child in self.children:
            n = child._searchNodeByRow(row)
            if n != None:
                return n
        return None