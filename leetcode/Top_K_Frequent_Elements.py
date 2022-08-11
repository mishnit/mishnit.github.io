# Given an array of elements (could be either strings or numbers) and an integer k, return the k most frequent elements.
# Tip: Use hashmap to count frequency
# Tip: Use frequency array of array to map frequency to list of items, index of array being frequency (min = 0, max = len)
# Tip: Avoid sorting and keep adding elements 


class Solution(object):
    def topKFrequent(self, elements, k):

        freq = [[] for i in range(len(elements) + 1)]
        
        count = {}
        for ele in elements:
            count[ele] = 1 + count.get(ele, 0)
        
        for ele, c in count.items():
            freq[c].append(ele)
        
        res = []
        
        for i in range(len(freq) - 1, 0, -1):
            for ele in freq[i]:
                res.append(ele)
                if len(res) == k:
                    return res
        # Above loop was O(n) only

    
class Test (object):
    def testtopKFrequent(self):
        s = Solution()
        #assert s.topKFrequent([1],1) == [1], "Fail"
        #assert s.topKFrequent([1,1,1,2,2,3],2) == [1,2], "Fail"
        assert s.topKFrequent(['wicket','ball','wicket','ball','bat','bat'],2) == ['bat','ball'], "Fail" #chronologically
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testtopKFrequent()

# O(n)
