# Given an array of strings, group the anagrams together.
# Tip: Use hashmap to keep sorted_word as key and group of anagram as value. preserve the order of words. 

class Solution (object):
    def groupAnagrams(self, strs):
        res = []
        dict = {}
        idx = 0
        for word in strs:
            sorted_word = ''.join(sorted(word))
            if sorted_word in dict:
                res[dict[sorted_word]].append(word)
            else:
                res.append([word])
                dict[sorted_word] = idx
                idx += 1
        return res

    
class Test (object):
    def testgroupAnagrams(self):
        s = Solution()
        assert s.groupAnagrams(['']) == [['']], "Fail"
        assert s.groupAnagrams(['a']) == [['a']], "Fail"
        assert s.groupAnagrams(['eat','tea','tan','ate','nat','bat']) == [['eat','tea','ate'],['tan','nat'],['bat']], "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testgroupAnagrams()

# O(nlgn)
