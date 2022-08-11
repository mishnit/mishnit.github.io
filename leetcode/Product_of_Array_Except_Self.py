class Solution(object):
    def productExceptSelf(self, nums):
        ans = [1] * len(nums)
        for i in range(1, len(nums)):
            ans[i] = ans[i - 1] * nums[i - 1]
        right = 1
        for i in range(len(nums) - 1, -1, -1):
            ans[i] = ans[i] * right
            right = right * nums[i]
        return ans
'''
Input:  [1,2,3,4]

Dynamic Programming trick:
Initial Output: [1,1,1,1]
After forward loop: [1,1,2,6]
After backward loop: [24,12,8,6]

Final Output: [24,12,8,6]
'''
