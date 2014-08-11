
ROW_TYPE = 0
START_POS = 1
END_POS = 2
LEVEL = 3
VALUE = 4

def getCSVRowType(row):
    return row[ROW_TYPE]

def getCSVRowStartPos(row):
    return row[START_POS].split(':')

def getCSVRowEndPos(row):
    return row[END_POS].split(':')

def getCSVRowLevel(row):
    return row[LEVEL]

def getCSVRowValue(row):
    if len(row) > VALUE:
        return row[VALUE]
    return ""
