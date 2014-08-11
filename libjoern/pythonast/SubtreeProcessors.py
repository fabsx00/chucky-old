
from libjoern.ASTNodeTypes import FUNCTION_NAME
from libjoern.csvast.CSVRowAccessors import getCSVRowValue


def getFunctionNameForFunction(node):
    for child in node.children:
        if child.row[0] == FUNCTION_NAME:
            return getCSVRowValue(child.row)
    raise


def getSubtreeValueFromNode(node, nodeType):
    if node.row[0] == nodeType:
        return node.row[4]
    for c in node.children:
        x = getSubtreeValueFromNode(c, nodeType)
        if x != None:
            return x
    return None

def getSubtree(node, nodeType):
    if node.row[0] == nodeType:
        return node
    for c in node.children:
        x = getSubtree(c, nodeType)
        if x != None:
            return x
    return None

def getAllSubtreesOfType(node, nodeTypes):
    nodes = []
    if node.getType() in nodeTypes:
        nodes.append(node)
    for c in node.children:
        nodes.extend(getAllSubtreesOfType(c, nodeTypes))
    return nodes
    
def getCalleeNodeForArgument(node):
    return node.parent.children[0]

def getCalleeNameForArgument(node):
    n = getCalleeNodeForArgument(node)
    return n.row[4]
    