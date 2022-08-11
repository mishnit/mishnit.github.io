# Given a sorted array, return sorted squares of these numbers (array can have negative numbers too)
# Tip: Use two pointers to keep track of min and max for absolute value of numbers

class Solution(object):
  def sortedSquares(self, nums):
    answer = [0] * len(nums)
    l = 0
    r = len(nums) - 1
    while l <= r:
        if abs(nums[l]) > abs(nums[r]):
            answer[r - l] = abs(nums[l]) * abs(nums[l])
            l += 1
        else:
            answer[r - l] = abs(nums[r]) * abs(nums[r])
            r -= 1
    return answer

class Test(object):
    def testsortedSquares(self):
        s = Solution()
        assert s.sortedSquares([-3,-2,0,1,5]) == [0,1,4,9,25], "test_1 failed"
        assert s.sortedSquares([-3,-2,-1,4]) == [1,4,9,16], "test_2 failed"
        print ("everything passed")

if __name__ == '__main__':
    t = Test()
    t.testsortedSquares()

    
# Time Complexity: O(N)
# Space Complexity: O(N)
