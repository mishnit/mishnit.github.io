class Solution(object):
    def maxSubArray(self, nums):
        chain_sum = max_sum = nums[0]
        for i in range(1, len(nums)):
            chain_sum = max(chain_sum + nums[i], nums[i])
            max_sum = max(max_sum, chain_sum)
        return max_sum
