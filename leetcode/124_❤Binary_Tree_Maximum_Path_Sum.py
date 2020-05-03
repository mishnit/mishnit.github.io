class Solution(object):
    def __init__(self):
        self.result = -(2**31)

    def maxPathSum(self, root):
        # return max(root.val, left.val+root.val, right.val+root.val, left.val+right.val+root.val)
        self.getNodeMaxValue(root)
        return self.result

    def getNodeMaxValue(self, node):
        # return node.val + max(left.val, right.val)
        if node is None:
            return 0
        lresult = self.getNodeMaxValue(node.left)
        rresult = self.getNodeMaxValue(node.right)
        self.result = max(lresult + rresult + node.val, self.result)
        ret = node.val + max(lresult, rresult)
        # if max left or right < 0 then return 0
        if ret > 0:
            return ret
        return 0
