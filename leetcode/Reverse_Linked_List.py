# Given the head of a singly linked list, reverse the list, and return the reversed list.

class LLNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def insertNode(self, data):
        if self.val:
            current = self
            while(current.next):
                current = current.next
            current.next = LLNode(data)
        else:
            self = LLNode(data)
            
    def insertNodes(self, datas):
        for data in datas:
                self.insertNode(data)
        
    def printLL(self):
        out =[]
        current = self
        while(current):
            out.append(current.val)
            current = current.next
        return out
    
class Solution(object):
    def reverseLL(self, head):
        if head is None or head.next is None:
            return head
        prev = None
        curr = head
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev
    
class Test (object):
    def testReverseLL(self, input, output):
        if len(input)!=0:
            LL = LLNode(input[0])
            if len(input)>0:
                LL.insertNodes(input[1:])
            s = Solution()
            LL = s.reverseLL(LL)
            assert LL.printLL() == output, "Fail"
        else:
            assert input == output, "Fail"
        
        
if __name__ == '__main__':
    t = Test()
    t.testReverseLL([1,2,3,4,5], [5,4,3,2,1])
    t.testReverseLL([1,2], [2,1])
    t.testReverseLL([], [])
    t.testReverseLL([0], [0])
    print "everything passed"
    
    
# O(n)
