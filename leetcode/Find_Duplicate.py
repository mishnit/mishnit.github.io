class Solution(object):
    def findDuplicate(self, nums):
        visited=set()
        for i in nums:
            if i not in visited:
                visited.add(i)
            else:
                return i

class Test(object):
    def testfindDuplicate(self):
        s = Solution()
        assert s.findDuplicate([1,3,4,2,2]) == 2, "test_1 failed"
        assert s.findDuplicate([3,1,3,4,2]) == 3, "test_2 failed"
        print ("everything passed")

if __name__ == '__main__':
    t = Test()
    t.testfindDuplicate()
