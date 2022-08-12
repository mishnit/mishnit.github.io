# You are given the heads of two sorted linked lists list1 and list2. Merge into single sorted linkedlist.

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
        if len(LL1_data)!=0 and len(LL2_data)!=0:
            LL1 = LLNode(LL1_data[0])
            if len(LL1_data)>0:
                LL1.insertNodes(LL1_data[1:])
            LL2 = LLNode(LL2_data[0])
            if len(LL2_data)>0:
                LL2.insertNodes(LL2_data[1:])
            s = Solution()
            LL3=LLNode()
            LL3 = s.mergeSortedLL(LL1,LL2)
            assert LL3.printLL() == merged_LL_data, "Fail"
        elif len(LL1_data)==0:
            assert LL2_data == merged_LL_data, "Fail"
        else:
            assert LL1_data == merged_LL_data, "Fail" 

        
if __name__ == '__main__':
    t = Test()
    t.testMergeSortedLL([1,2,4], [1,3,4], [1,1,2,3,4,4])
    t.testMergeSortedLL([], [], [])
    t.testMergeSortedLL([], [0], [0])
    print "everything passed"
    
# O(n)
