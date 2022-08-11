# Given an array of +/- integers, find all unique triplets whose sum is equal to K 
# Tip: This problem is different from TwoSum as we were identifying indices of duplet earlier & only one duplet existed
# Tip: Here multiple triplets may exist and we need to identify all triplets rather their indices 
import copy

class Solution(object):
    def modifiedTwoSum(self, nums, target): # find all duplets whose sum is equal to target
        all_duplets = []
        d={}
        for num in nums:
            if target-num in d:
                d.pop(target-num, None)
                all_duplets.append([target-num, num])
            else:
                d[num]=True
        return all_duplets
    
    def threeSum(self, nums, k): # find all triplets whose sum is equal to k
        all_triplets = []
        d={}
        for num in nums:
            new = copy.deepcopy(nums)
            new.remove(num)
            duplets = self.modifiedTwoSum(new,k-num)
            if len(duplets) != 0:
                for duplet in duplets:
                    duplet.append(num)
                all_triplets.append(duplet)
        all_triplets = list(map(list, (set(map(lambda x: tuple(sorted(x)), all_triplets))))) #remove duplicate triplets
        return all_triplets
    
class Test (object):
    def testModifiedTwoSum(self):
        s = Solution()
        assert s.modifiedTwoSum([3, 2, 4, 3, 4], 6) == [[2,4], [3,3]], "Fail"
        print "everything passed - Modified Two Sum"

    def testThreeSum(self):
        s = Solution()
        assert s.threeSum([0,1,1], 0) == [], "Fail"
        assert s.threeSum([0,0,0], 0) == [[0,0,0]], "Fail" # only one such triplet
        assert s.threeSum([3, 2, 4, 3, 4, 0], 8) == [[2,3,3], [0,4,4]], "Fail" # two such triplets
        assert s.threeSum([-1,0,1,2,-1,-4], 0) == [[-1,-1,2],[-1,0,1]], "Fail" # two such triplets
        print "everything passed - Three Sum"
        
if __name__ == '__main__':
    t = Test()
    t.testModifiedTwoSum()
    t.testThreeSum()

# O(n^2)
