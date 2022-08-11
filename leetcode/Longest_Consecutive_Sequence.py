# Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
# Tip: use set to find unique elements then check if its start of a new sequence and compute length_so_far for the sequence 

class Solution(object):
    def lengthLCS(self, nums):
        numset = set(nums)
        longest = 0

        for num in nums:
            # check if its the start of a sequence, reset length_so_far to 1
            if (num - 1) not in numset:
                length_so_far = 1
                while (num + length_so_far) in numset:
                    length_so_far += 1
                longest = max(length_so_far, longest)
        return longest

    
class Test (object):
    def testLengthLCS(self):
        s = Solution()
        assert s.lengthLCS([100,4,200,1,3,2]) == 4, "Fail"
        assert s.lengthLCS([0,3,7,2,5,8,4,6,0,1]) == 9, "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testLengthLCS()

# O(n)
