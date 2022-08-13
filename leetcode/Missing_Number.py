# Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.

class Solution(object):
    def missingNumber(self, nums):
        res = len(nums)
        for i in range(len(nums)):
            res += i - nums[i]
        return res
        
    
class Test (object):
    def testMissingNumber(self, sequence, number):
        s = Solution()
        assert s.missingNumber(sequence) == number, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMissingNumber([3,0,1], 2)
    t.testMissingNumber([0,1], 2)
    t.testMissingNumber([9,6,4,2,3,5,7,0,1], 8)
    print "everything passed"
    
# O(n)
