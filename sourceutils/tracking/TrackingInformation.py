
class TrackingInformation:
    def __init__(self):
        self.typeToIdentifier = dict()
        self.identifierToType = dict()
        self.parameters = []
        self.locals = []
        self.functionArguments = dict()
        self.functionsConsuming = dict()
        self.lvalToRval = dict()
        self.rvalToLval = dict()
        
        self.lvalToExpr = dict()

    def addTypeIdentifierMap(self, typeName, identifier):
        try:
            self.typeToIdentifier[typeName].append(identifier)
        except:
            self.typeToIdentifier[typeName] = [identifier]
        
        try:
            self.identifierToType[identifier].append(typeName)
        except:
            self.identifierToType[identifier] = [typeName]
    
    def addAssignMap(self, lval, rval):
        try:
            self.lvalToRval[lval].append(rval)
        except:
            self.lvalToRval[lval] = [rval]
        try:
            self.rvalToLval[rval].append(lval)
        except:
            self.rvalToLval[rval] = [lval]

    def addRvalExpr(self, lval, rvalExpr):
        try:
            self.lvalToExpr[lval].append(rvalExpr)
        except:
            self.lvalToExpr[lval] = [rvalExpr]
        