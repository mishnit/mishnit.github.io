class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        stack = []
        d = {}
        for num in nums2:
            while stack and num > stack[-1]:
                top = stack.pop()
                d[top] = num
            stack.append(num)
        res = []
        for num in nums1:
            res.append(d.get(num, -1))
        return res

class Test(object):
    def testnextGreaterElement(self):
        s = Solution()
        assert s.nextGreaterElement([4,1,2], [1,3,4,2]) == [-1,3,-1], "test_1 failed"
        assert s.nextGreaterElement([2,4], [1,2,3,4]) == [3,-1], "test_2 failed"
        print ("everything passed")

if __name__ == '__main__':
    t = Test()
    t.testnextGreaterElement()
