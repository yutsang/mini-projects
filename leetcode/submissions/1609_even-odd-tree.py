# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        
        queue = deque([root])
        level = 0
        
        while queue:
            size = len(queue)
            prev = None
            
            for _ in range(size):
                node = queue.popleft()
                
                if level % 2 == 0:  
                    if node.val % 2 == 0:  
                        return False
                    if prev and node.val <= prev:  
                        return False
                else:  
                    if node.val % 2 == 1:  
                        return False
                    if prev and node.val >= prev:  
                        return False
                
                prev = node.val
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            level += 1
        
        return True
        