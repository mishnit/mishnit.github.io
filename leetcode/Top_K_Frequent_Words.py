# Given an array of elements (could be either strings or numbers) and an integer k, return the k most frequent elements.
# Tip: Use hashmap to count frequency

class Solution(object):
    def topKFrequent(self, elements, k):
        count = {}
        freq = [[] for i in range(len(elements) + 1)]

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
    
class Test (object):
    def testtopKFrequent(self):
        s = Solution()
        assert s.topKFrequent([1],1) == [1], "Fail"
        assert s.topKFrequent([1,1,1,2,2,3],2) == [1,2], "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testtopKFrequent()
