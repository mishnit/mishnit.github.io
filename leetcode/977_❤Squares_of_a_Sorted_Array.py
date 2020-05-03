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

# Time Complexity: O(N)
# Space Complexity: O(N)
