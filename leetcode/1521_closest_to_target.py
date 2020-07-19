# https://leetcode.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/

class Solution(object):
    def closestToTarget(self, arr, target):
        min_diff = abs(target - arr[0])
        print(min_diff)
        trials = set()
        for a in arr:
            if not min_diff:
                return 0
            trials.add(a)
            tn = set()
            for t in trials:
                ta = t & a
                min_diff = min(min_diff, abs(target - ta))
                if ta > target:
                    tn.add(ta)
            trials = tn
        return min_diff
