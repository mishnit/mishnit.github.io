# Given the root of a binary tree, return the maximum path sum. (one leaf node to another leaf node via any node(s))

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
    def __init__(self):
        self.result = -(2**31)

    def maxPathSum(self, root):
        # return max(root.val, left.val+root.val, right.val+root.val, left.val+right.val+root.val)
        self.getNodeMaxValue(root)
        return self.result

    def getNodeMaxValue(self, node):
        # return node.val + max(left.val, right.val)
        if node:
            lresult = self.getNodeMaxValue(node.left)
            rresult = self.getNodeMaxValue(node.right)
            if node.val is None:
                node.val = 0
            self.result = max(lresult + rresult + node.val, self.result)
            ret = node.val + max(lresult, rresult)
            # if max left or right < 0 then return 0
            if ret > 0:
                return ret
            return 0
        else:
            return 0

    
class Test (object):
    def testMaxPathSum(self, Actual_Tree_Data, Max_Path_Sum):
        if len(Actual_Tree_Data)!=0:
            root = TreeNode(Actual_Tree_Data[0])
            if len(Actual_Tree_Data)>0:
                root.insertNodes(Actual_Tree_Data[1:])
            s= Solution()
            output = s.maxPathSum(root)
            assert output == Max_Path_Sum, "Fail"
        else:
            assert 0 == Max_Path_Sum, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMaxPathSum([1,2,3], 6)
    t.testMaxPathSum([-10,9,20,None,None,15,7], 42)
    print "everything passed"
    
# O(n)
