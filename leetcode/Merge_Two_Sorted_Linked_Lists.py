# You are given the heads of two sorted linked lists list1 and list2. Merge into single sorted linkedlist.

class LLNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self, head=None):  
        self.head = head

    def insertNode(self, data):
        newNode = LLNode(data)
        if(self.head):
            current = self.head
            while(current.next):
                current = current.next
            current.next = newNode
        else:
            self.head = newNode
            
    def insertNodes(self, datas):
        for data in datas:
            self.insertNode(data)

    def printLL(self):
        out =[]
        current = self.head
        while(current):
            out.append(current.val)
            current = current.next
        return out

class Solution(object):
    def mergeSortedLL(self, head1, head2):
        dummy = LLNode()
        tail = dummy
        while head1 and head2:
            if head1.val < head2.val:
                tail.next = head1
                head1 = head1.next
            else:
                tail.next = head2
                head2 = head2.next
            tail = tail.next
        if head1:
            tail.next = head1
        elif head2:
            tail.next = head2
        return dummy.next
    
class Test (object):
    def testMergeSortedLL(self, LL1_data, LL2_data, merged_LL_data):
        LL1 = LinkedList()
        LL1.insertNodes(LL1_data)
        LL2 = LinkedList()
        LL2.insertNodes(LL2_data)
        s = Solution()
        LL3 = LinkedList(s.mergeSortedLL(LL1.head,LL2.head))
        assert LL3.printLL() == merged_LL_data, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMergeSortedLL([1,2,4], [1,3,4], [1,1,2,3,4,4])
    t.testMergeSortedLL([], [], [])
    t.testMergeSortedLL([], [0], [0])
    print "everything passed"
    
# O(n)
