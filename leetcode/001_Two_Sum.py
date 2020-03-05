class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i in range(len(nums)):
            other = target - nums[i]
            if other in seen:
                return [seen[other], i]
            else:
                seen[nums[i]] = i
        return []
        
if __name__ == '__main__':
    # begin
    s = Solution()
    print s.twoSum([3, 2, 4], 6)
