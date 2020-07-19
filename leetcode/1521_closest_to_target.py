# https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/

class Solution(object):
    def closestToTarget(self, arr, target):
        s, ans = set(), float('inf')
        for a in arr:
            s = {a & b for b in s} | {a}
            for a in s:
                ans = min(ans, abs(a - target))
        return ans
