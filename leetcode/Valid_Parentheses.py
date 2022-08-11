# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine all parenthesis are valid
# Tip: Use hashmap to create closing to open parenthesis mapping and use stack to push pop

class Solution(object):
    def isValid(self, s):
        
        hashmap = { "]":"[", "}":"{", ")":"(" }
        stack = []
        for char in s:
            if char in hashmap.values():
                stack.append(char)
            elif char in hashmap.keys():
                if stack == [] or hashmap[char] != stack.pop():
                    return False
            else:
                return False
        return stack == []
        
    
class Test (object):
    def testIsValid(self):
        s = Solution()
        assert s.isValid("()") == True, "Fail"
        assert s.isValid("()[]{}") == True, "Fail"
        assert s.isValid("(]") == False, "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testIsValid()
    
# O(n)
