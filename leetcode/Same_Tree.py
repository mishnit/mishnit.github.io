# Given the roots of two binary trees p and q, write a function to check if they are the same or not.

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
    def areTreeSame(self, root1, root2):
        if not root1 and not root2:
            return True
        if root1 and root2 and root1.val == root2.val:
            return self.areTreeSame(root1.left, root2.left) and self.areTreeSame(root1.right, root2.right)
        else:
            return False            
    
class Test (object):
    def testAreTreeSame(self, Tree1_Data, Tree2_Data, output):
        if len(Tree1_Data)!=0 and len(Tree2_Data)!=0:
            root1 = TreeNode(Tree1_Data[0])
            if len(Tree1_Data)>0:
                root1.insertNodes(Tree1_Data[1:])
            root2 = TreeNode(Tree2_Data[0])
            if len(Tree2_Data)>0:
                root2.insertNodes(Tree2_Data[1:])
            s= Solution()
            result = s.areTreeSame(root1, root2)
            assert result == output, "Fail"
        else:
            assert 0 == output, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testAreTreeSame([1,2,3], [1,2,3], True)
    t.testAreTreeSame([1,2], [1, None, 2], False)
    t.testAreTreeSame([1,2,1], [1, 1, 2], False)
    print "everything passed"
    
# O(n)
