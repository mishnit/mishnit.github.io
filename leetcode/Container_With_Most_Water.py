# Given heights of the bars inside the container, Return the maximum amount of water a container can store 
# Tip: choose two lines such that we could maximize the min of two heights and the distance between the bars.

class Solution(object):
    def maxArea(self, heights):
        l, r = 0, len(heights) - 1
        result = 0

        while l < r:
            result = max(result, min(heights[l], heights[r]) * (r - l))
            if heights[l] < heights[r]:
                l += 1
            elif heights[r] <= heights[l]:
                r -= 1
        return result
        
    
class Test (object):
    def testMostWater(self):
        s = Solution()
        assert s.maxArea([1,1]) == 1, "Fail"
        assert s.maxArea([1,8,6,2,5,4,8,3,7]) == 49, "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testMostWater()


# O(n)
