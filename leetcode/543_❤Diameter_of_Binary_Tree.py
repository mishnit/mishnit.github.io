# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def diameterOfBinaryTree(self, root):
        self.diameter = 0
        self.depth(root)
        return self.diameter    
    
    def depth(self, root):
        if root is None:
            return 0
        left = self.depth(root.left)
        right = self.depth(root.right)
        self.diameter = max(self.diameter, left + right)
        height = max(left, right) + 1
        return height
