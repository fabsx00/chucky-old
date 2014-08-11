import cPickle as pickle
from sourceutils.misc.GzipPickler import GzipPickler
from sourceutils.tracking.TrackingInformation import TrackingInformation
from libjoern.pythonast.PythonASTProcessor import PythonASTProcessor

from libjoern.ASTNodeTypes import PARAMETER_DECL, VAR_DECL, ASSIGN
from libjoern.ASTNodeTypes import ARGUMENT, CALLEE, FIELD
from libjoern.pythonast.SubtreeProcessors import getSubtreeValueFromNode, getSubtree
from libjoern.pythonast.SubtreeProcessors import getCalleeNameForArgument, getAllSubtreesOfType


class TrackingInformationGenerator(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
        self._registerHandlers()
    
    def _callHandlers(self, node):
        nodeType = node.row[0]
        if nodeType in self.handlers:
            handler = self.handlers[nodeType]
            return handler(node)
        return True
    
    def _registerHandlers(self):
        self.handlers[PARAMETER_DECL] = self.parameterAndLocalDeclHandler
        self.handlers[VAR_DECL] = self.parameterAndLocalDeclHandler
        self.handlers[ASSIGN] = self.assignmentHandler
        self.handlers[ARGUMENT] = self.argumentHandler
        
    def reset(self, location):
        self.trackingInfo = TrackingInformation()
        self.originalAST = self._getASTForLocation(location)
        self.outputFilename = location + '/tracking_info.pickl'

    def process(self):
        self.processChildren(self.originalAST)

    def save(self):
        pickle.dump(self.trackingInfo, file(self.outputFilename, 'w'), protocol=2)

    def _getASTForLocation(self, location):
        return GzipPickler().load(location + '/func_ast.pickl')
    
    def parameterAndLocalDeclHandler(self, node):
        typeName = getSubtreeValueFromNode(node, 'TYPE')
        localName = getSubtreeValueFromNode(node, 'NAME')
        if localName:
            self.trackingInfo.addTypeIdentifierMap(typeName, localName)
        
        if node.getType() == PARAMETER_DECL:
            self.trackingInfo.parameters.append(localName)
        else:
            self.trackingInfo.locals.append(localName)

        return True
    
    def assignmentHandler(self, node):
        lval = getSubtreeValueFromNode(node, 'LVAL')
        rvalNode = getSubtree(node, 'RVAL')
        self.trackingInfo.addRvalExpr(lval, rvalNode)
        
        rvals = self.rvalTraverseChildren(rvalNode)
    
        for rval in rvals:
            self.trackingInfo.addAssignMap(lval, rval)
        return True
    
    def rvalTraverseChildren(self, node):
        l = []
        for c in node.children:
            l.extend(self.rvalTraverse(c))
        return l
    
    def rvalTraverse(self, node):
        nodeType = node.row[0]
        l = []
        
        if nodeType == ARGUMENT:
            # do not enter arguments of calls
            return []
        elif nodeType in [CALLEE, FIELD]:
            # FIXME
            l.append(node.row[4])
        
        l.extend(self.rvalTraverseChildren(node))
        
        return l
    
    def argumentHandler(self, node):
        callee = getCalleeNameForArgument(node)
        subtrees = getAllSubtreesOfType(node, ['UNARY_EXPR', 'FIELD'])
        
        for subtree in subtrees:
            if subtree.getType() == 'FIELD':
                if subtree.parent.getType() != 'UNARY_EXPR':
                    self.addArgument(callee, subtree.row[4])
            else:
                self.addArgument(callee, subtree.row[4])
            
        return True

    def addArgument(self, funcName, argument):
        try:
            self.trackingInfo.functionArguments[funcName].append(argument)
        except KeyError:
            self.trackingInfo.functionArguments[funcName] = [argument]
        
        try:
            self.trackingInfo.functionsConsuming[argument].append(funcName)
        except KeyError:
            self.trackingInfo.functionsConsuming[argument] = [funcName]
        