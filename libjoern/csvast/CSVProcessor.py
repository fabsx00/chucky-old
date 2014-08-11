import csv
from CSVRowAccessors import getCSVRowType

MAX_CSV_FIELD_SIZE = 131072*100

class CSVProcessor:
    def __init__(self):
        self.handlers = dict()
        self.defaultHandler = None
        
        self.reader = None
        self.currentFile = None
    
    def processCSVRows(self, metaDataFile):
        self.currentFile = metaDataFile
        csv.field_size_limit(MAX_CSV_FIELD_SIZE)
        self.reader = csv.reader(open(metaDataFile), delimiter="\t",
                            quotechar=None, escapechar=None)
        
        for row in self.reader:
            self._processCSVRow(row)
        
    def _processCSVRow(self, row):
        
        if self.defaultHandler:
            executeOtherHandlers = self.defaultHandler(row)
            if not executeOtherHandlers: return
        
        lineType = getCSVRowType(row)
        handler = self._getHandlerForType(lineType)
        if not handler: return
        handler(row)

    def registerChildHandler(self, level, childHandler):
        self.parentLevel = level
        self.defaultHandler = childHandler
    
    def unregisterChildHandler(self):
        self.parentLevel = None
        self.defaultHandler = None

    def _getHandlerForType(self, lineType):
        try:
            return self.handlers[lineType]
        except:
            return None