# https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/

class Solution(object):
    def closestToTarget(self, arr, target):
        a = set([arr[0]])
        stk = set([arr[0]])
        for i in range(1,len(arr)):
            tmp = set()
            tmp.add(arr[i])
            a.add(arr[i])
            for j in stk:
                x = j&arr[i]
                tmp.add(x)
                a.add(x)
        ans = abs(target-1000000000)
        for i in a:
            if abs(i- target) < ans:
                ans = abs(i - target)
        return ans
