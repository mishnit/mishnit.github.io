class Solution(object):
    def canJump(self, nums):
        length = len(nums)
        last = length - 1
        for i in reversed(range(length - 1)):
            if i + nums[i] >= last:
                last = i
        return not last

'''
Time Complexity: O(n)
Space Complexity: O(1)
'''
