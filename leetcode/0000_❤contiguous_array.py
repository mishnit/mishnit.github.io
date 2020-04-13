# Given a binary array, find the maximum length of a contiguous subarray with equal number of 0 and 1.

class Solution(object):
    def findMaxLength(self, nums):
        s,d,m = 0,{0:-1},0 # Vars for sum, dict having (sum, first_index_for_this_sum) and current longest subarray length
        for i,v in enumerate(nums): # scanning through the array using index i and value v
            if v == 1:
                s += 1
            elif v == 0:
                s -= 1
            if s in d: # have we seen same sum of 0/1s before?
                m = max(m,i-d[s]) # yes, update max length
            else:
                d[s] = i        # no, this is the first time, let's add that index for that sum
        return m  # return the largest length
        
# Hint: calculate neutralized sum of elements (starting from first element) at each index.
# If any value of neutralized sum repeats for index i and j, that means all elements have occurred equally from ith to jth index.
