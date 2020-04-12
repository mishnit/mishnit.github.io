class Solution(object):
    def moveZeroes(self, nums):
        for zero_idx in range(0, len(nums)):
            if nums[zero_idx] == 0:
                break
            else:
                zero_idx += 1
        for i in range(zero_idx, len(nums)):
            if nums[i] != 0:
                temp = nums[zero_idx]
                nums[zero_idx] = nums[i]
                nums[i] = temp
                zero_idx += 1
        return nums
