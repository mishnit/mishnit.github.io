# Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
# Tip: In first pass, compute product of all elements left to self
# Tip: In second pass, compute product of all elements right to self

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

    
class Test (object):
    def testProductExceptSelf(self):
        s = Solution()
        assert s.productExceptSelf([1,2,3,4]) == [24,12,8,6], "Fail"
        assert s.productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0], "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testProductExceptSelf()

# O(n)
