class Solution(object):
    def rangeBitwiseAnd(self, m, n):
        while n > m:
            n &= (n-1)
        return m & n
