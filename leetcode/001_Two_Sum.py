class Solution:
    def twoSum(self, nums, target):
        map = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if map.get(complement) != None:
                return [map[complement], i]
            map[nums[i]] = i

        return "no answer"
        
if __name__ == '__main__':
    # begin
    s = Solution()
    print s.twoSum([3, 2, 4], 6)
