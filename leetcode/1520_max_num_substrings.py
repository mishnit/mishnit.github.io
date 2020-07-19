https://leetcode.com/problems/maximum-number-of-non-overlapping-substrings/

import heapq

class Solution:
    def maxNumOfSubstrings(self, s):
        first = {}
        last = {}
        for i in range(len(s)):
            c = s[i]
            last[c] = i
        for i in range(len(s)-1,-1,-1):
            c = s[i]
            first[c] = i
        intervals = set()
        lookup = {}
        for c in first:
            st = first[c]
            ed = last[c]
            visible = set()
            for i in range(st,ed+1):
                visible.add(s[i])
            lookup[c] = visible
        for c in first:
            seen = set()
            def dfs(cur,seen):
                seen.add(cur)
                for n in lookup[cur]:
                    if n not in seen:
                        dfs(n,seen)
            dfs(c,seen)
            lower = min(first[c] for c in seen)
            upper = max(last[c] for c in seen)
            intervals.add((lower, upper))
        pq = []
        intervals = list(intervals)
        intervals.sort(key = lambda x : x[1] - x[0])
        ans = []
        taken = set()
        for a,b in intervals:
            if any(x in taken for x in range(a,b+1)):
                continue
            taken.add(a)
            taken.add(b)
            ans.append(s[a:b+1])
        return ans
