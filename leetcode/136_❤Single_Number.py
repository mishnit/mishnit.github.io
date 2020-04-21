class Solution(object):
    def singleNumber(self, nums):
        res = 0
        for num in nums:
            res ^= num
        return res
"""    
Hint: XOR
Time Complexity: O(n)
Space Complexity: O(1)
"""
