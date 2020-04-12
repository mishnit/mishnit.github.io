def back(res,c):
    if c == '#':
        return res[:-1]
    return res+c

class Solution(object):
    def backspaceCompare(self, S, T):
        #calling recursion on S
        res_c = ""
        for c in S:
            res_c = back(res_c, c)
        #calling recursion on T
        res_t = ""
        for c in T:
            res_t = back(res_t, c)
        return res_c == res_t
# Time: O(N)
# Space: O(1)
