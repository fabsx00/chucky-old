
class TreeToStringsConverter:
    def __init__(self):
        pass
    
    def leafNodeToString(self, node):
        """ Override """
        return ''
    
    def nonLeafNodeToString(self, node, immediateChildStrings):
        """ Override """
        return ''
    
    def includeLeafNode(self, node):
        """ Override """
        return True
        
    def skipChildExpansion(self, child):
        """ Override """
        return False
    
    def allSubtreesAsString(self, tree):
        
        (e, expressions) = self._allSubtreesAsString(tree)
        return expressions
    
    def _allSubtreesAsString(self, node):
        
        if node.hasNoChildren():
            
            thisNodesStr = self.leafNodeToString(node)
            
            if not self.includeLeafNode(node):
                return (thisNodesStr, [])
                        
            return (thisNodesStr, [thisNodesStr]) 
        else:
            
            allStrings = []
            immediateChildStrings = []
            
            for child in node.children:
                if self.skipChildExpansion(child):
                    continue
                (childString, childsChildren) = self._allSubtreesAsString(child)
                  
                immediateChildStrings.append(childString)
                allStrings.extend(childsChildren)
        
            thisNodesStr = self.nonLeafNodeToString(node, immediateChildStrings)
            allStrings.append(thisNodesStr)
            return (thisNodesStr, allStrings)
      