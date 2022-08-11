# Does Given Array contains Duplicate?
# Tip: Use set to check duplicate 

class Solution (object):
    def hasDuplicate(self, nums):
        return len(nums) != len(set(nums))
    
class Test (object):
    def testhasDuplicate(self):
        s = Solution()
        assert s.hasDuplicate([2,2,3]) == True, "Fail"
        assert s.hasDuplicate([2,3]) == False, "Fail"
        print "evrything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testhasDuplicate()
