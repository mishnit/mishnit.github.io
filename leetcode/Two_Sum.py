# Return indices of two unique numbers whose sum is equal to target (Only one guaranteed solution exist)
# Tip: Convert array into tuple using enumerate and use hashmap to find value and track indices of num and target minus num 

class Solution(object):
    def twoSum(self, nums, target):
        d={}
        for i,num in enumerate(nums):
            if target-num in d:
                return [d[target-num], i]
            d[num]=i
    
class Test (object):
    def testTwoSum(self):
        s = Solution()
        assert s.twoSum([3, 2, 4], 6) == [1,2], "Fail"
        assert s.twoSum([2, 7, 11, 15], 9) == [0,1], "Fail"
        assert s.twoSum([3, 3], 6) == [0,1], "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testTwoSum()
