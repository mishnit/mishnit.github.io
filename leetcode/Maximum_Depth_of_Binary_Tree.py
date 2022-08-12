# Given the root of a binary tree, return its maximum depth.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def insertNode(self, data): #level order insertion
        if self:
            q = []
            q.append(self)
            while (len(q)):
                temp = q[0]
                q.pop(0)
                if (not temp.left):
                    temp.left = TreeNode(data)
                    break
                else:
                    q.append(temp.left)
 
                if (not temp.right):
                    temp.right = TreeNode(data)
                    break
                else:
                    q.append(temp.right)

    def insertNodes(self, datas):
        for data in datas:
            self.insertNode(data)

class Solution(object):
    def maxDepth(self, root):
        if root is None:
            return 0
        ld = self.maxDepth(root.left)
        rd = self.maxDepth(root.right)
        return 1 + max(ld, rd)
    
    def printLevelOrder(self, root): #Breadth First Traversal
        if root is None:
            return
        queue = []
        out=[]
        queue.append(root)
        while(len(queue) > 0):
            out.append(queue[0].val)
            node = queue.pop(0)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return out
    
class Test (object):
    def testMaxDepth(self, Actual_Tree_Data, output):
        if len(Actual_Tree_Data)!=0:
            root = TreeNode(Actual_Tree_Data[0])
            if len(Actual_Tree_Data)>0:
                root.insertNodes(Actual_Tree_Data[1:])
            s= Solution()
            result = s.maxDepth(root)
            assert result == output, "Fail"
        else:
            assert 0 == output, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMaxDepth([3,9,20,None,None,15,7], 3)
    t.testMaxDepth([1,None,2], 2)
    print "everything passed"
    
# O(n)
