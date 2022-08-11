# Check if given string is a palindrome
# Tip: Remove all non alphanumeric characters. Find mid of the string and check if all prev and next to mid are matching

class Solution(object):
    def isPalindrome(self, str):
        alnum_str = [t.lower() for t in str if t.isalnum()]
        if len(alnum_str) <= 1:
            return True
        mid = len(alnum_str) / 2
        for i in range(mid):
            if alnum_str[i] != alnum_str[len(alnum_str) - 1 - i]:
                return False
        return True

    
class Test (object):
    def testIsPalindrome(self):
        s = Solution()
        assert s.isPalindrome("") == True, "Fail"
        assert s.isPalindrome("A man, a plan, a canal: Panama") == True, "Fail" # "amanaplanacanalpanama"
        assert s.isPalindrome("race a car") == False, "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testIsPalindrome()

# O(n)
