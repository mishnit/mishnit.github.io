class Solution(object):
    def search(self, nums, target):
        l = len(nums) 
        low = 0
        high = l-1
        while low <= high:
            center = (low + high) // 2
            if nums[center] == target:
                return center
            if nums[low] < nums[center]: #lhs is sorted
                if nums[low] <= target and (center == 0 or nums[center-1] >= target):
                    high = center - 1
                else:
                    low = center + 1
            else: #rhs is sorted
                if (center == l-1 or nums[center+1] <= target) and nums[high] >= target:
                    low = center + 1
                else:
                    high = center - 1               
        return -1
