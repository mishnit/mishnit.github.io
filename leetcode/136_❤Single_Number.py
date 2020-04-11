class Solution(object):
    def singleNumber(self, nums):
        # xor
        res = 0
        for num in nums:
            res ^= num
        return res
