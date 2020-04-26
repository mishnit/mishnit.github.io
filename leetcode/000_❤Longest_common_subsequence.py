class Solution(object):
    def longestCommonSubsequence(self, text1, text2):
        n = len(text1) + 1
        m = len(text2) + 1
        dp = [0] * m    # assuming text2 is smaller than text1
        for i in range(1, n):
            prev = 0
            for j in range(1, m):
                last = dp[j]
                if text1[i-1] == text2[j-1] and prev+1 > last:
                    dp[j] = prev + 1
                else:
                    prev = max (prev, last)
        return max(dp)
        
'''
Time: O(m * n)
Space: O(min(m, n))
'''
