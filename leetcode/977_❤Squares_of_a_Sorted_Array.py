class Solution(object):
  def sortedSquares(self, A):
    answer = [0] * len(A)
    l = 0
    r = len(A) - 1
    while l <= r:
        left, right = abs(A[l]), abs(A[r])
        if left > right:
            answer[r - l] = left * left
            l += 1
        else:
            answer[r - l] = right * right
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
