class Solution(object):
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
