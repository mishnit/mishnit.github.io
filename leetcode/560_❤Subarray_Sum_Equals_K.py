class Solution(object):
    def subarraySum(self, nums, k):
        n = len(nums)
        curr_sum = 0
        ans = 0
        sum_dict = {0: 1}
        for i in range(n):
            curr_sum += nums[i]
            if curr_sum - k in sum_dict:
                ans += sum_dict[curr_sum-k]
            if curr_sum in sum_dict:
                sum_dict[curr_sum] += 1
            else:
                sum_dict[curr_sum] = 1
        return ans

'''
Time Compleity: O(n)
Space Complecity: O(n)
'''
