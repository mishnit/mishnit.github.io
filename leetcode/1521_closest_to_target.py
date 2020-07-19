# https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/

class Solution:
    def closestToTarget(self, arr: List[int], target: int) -> int:
        a = set([arr[0]])
        stk = set([arr[0]])
        for i in range(1,len(arr)):
            tmp = set()
            tmp.add(arr[i])
            a.add(arr[i])
            for j in stk:
                _ = j&arr[i]
                tmp.add(_)
                a.add(_)
        ans = abs(target-1000000000)
        for i in a:
            if abs(i- target) < ans:
                ans = abs(i - target)
        return ans
