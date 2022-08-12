# Given the head of a linked list, remove the nth node from the end of the list and return its head.

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
    
class Solution:
    def removeNthFromEnd(self, head, n):
        if head is None:
            return None
        slow = fast = head
        for i in range(n):
            fast = fast.next
        if fast is None:
            head = head.next
            return head
        while fast.next is not None:
            fast = fast.next
            slow = slow.next
        curr = slow.next
        slow.next = curr.next
        return head
    
class Test (object):
    def testRemoveNthFromEnd(self, LL_data, n, output):
        if len(LL_data)!=0 and n<=len(LL_data):
            LL = LLNode(LL_data[0])
            if len(LL_data)>0:
                LL.insertNodes(LL_data[1:])
            s = Solution()
            LLnew = s.removeNthFromEnd(LL,n)
            if LLnew == None:
                assert []==output, "Fail"
            else:    
                assert LLnew.printLL()==output, "Fail"
        else:
            assert LL_data == output, "Fail"
        
        
if __name__ == '__main__':
    t = Test()
    t.testRemoveNthFromEnd([1,2,3,4,5], 2, [1,2,3,5])
    t.testRemoveNthFromEnd([1], 1, [])
    t.testRemoveNthFromEnd([1,2], 1, [1])
    print "everything passed"
    
    
# O(n)
