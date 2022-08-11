# Are Given 2 Strings Anagram of each other?
# Tip: Use hashmap to count frequency 

class Solution (object):
    def isAnagram(self, str1, str2):
        if len(str1) != len(str2):
            return False
        
        freq_str1 = {}
        freq_str2 = {}
        
        for i in range(len(str1)):
            freq_str1[str1[i]] = freq_str1.get(str1[i],0) +1
            freq_str2[str2[i]] = freq_str2.get(str2[i],0) +1
        return freq_str1 == freq_str2
    
class Test (object):
    def testisAnagram(self):
        s = Solution()
        assert s.isAnagram("okay","ok") == False, "Fail"
        assert s.isAnagram("popo","oppo") == True, "Fail"
        assert s.isAnagram("popo","coco") == False, "Fail"
        print "evrything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testisAnagram()


# Tip2: Just sort and check  

# class Solution (object):
#     def isAnagram(self, str1, str2):
#         return sorted(str1) == sorted(str2)
