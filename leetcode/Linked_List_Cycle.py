# Given the head of a linked list, determine if the linked list has a cycle in it.

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
                
    def updateTail(self, tail_index):
        if self.val and tail_index>=0:
            current = self
            while(current.next):
                current = current.next
            tail = self
            for i in range(tail_index):
                tail = tail.next
            current.next = tail
        
    def printLL(self):
        out =[]
        current = self
        while(current):
            out.append(current.val)
            current = current.next
        return out
    
class Solution(object):
    def hasCycle(self, head):
            fast = head
            slow = head
            while fast and fast.next:
                fast = fast.next.next
                slow = slow.next
                if slow == fast:
                    return True
            return False
    
class Test (object):
    def testHasCycle(self, LL_data, tail_index, output):
        if len(LL_data)!=0:
            LL = LLNode(LL_data[0])
            if len(LL_data)>0:
                LL.insertNodes(LL_data[1:])
            LL.updateTail(tail_index)
            s = Solution()
            assert s.hasCycle(LL)==output, "Fail"
        else:
            assert False == output, "Fail"
        
        
if __name__ == '__main__':
    t = Test()
    t.testHasCycle([3,2,0,-4], 0, True)
    t.testHasCycle([1,2], 0, True)
    t.testHasCycle([1], 1, False)
    t.testHasCycle([], 2, False)
    print "everything passed"
    
    
# O(n)
