# class Solution(object):
#     def maxArea(self, height):
#         """
#         :type height: List[int]
#         :rtype: int
#         """
class Solution(object):
#     def maxArea(self, height):
#         # brute force
#         ls = len(height)
#         left, right = 0, ls - 1
#         result = 0
#         while left < right:
#             result = max(min(height[left], height[right]) * (right - left), result)
#             if height[left] > height[right]:
#                 right -= 1
#             else:
#                 left += 1
#         return result

    def maxArea(self, height):
        # skip some choices
        ls = len(height)
        lm = min(height[0], height[ls - 1])
        max_v = lm * (ls - 1)
        low = 0
        high = ls - 1
        while low < high:
            while height[low] < lm and low < ls:
                low += 1
            while height[high] < lm and high < ls:
                high -= 1
            if low > high:
                break
            m = min(height[low], height[high])
            if m * (high - low) > max_v:
                max_v = m * (high - low)
                lm = m
            if height[low] < height[high]:
                low += 1
            else:
                high -= 1
        return max_v