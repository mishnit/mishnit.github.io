# Given the head of a singly linked list, reverse the list, and return the reversed list.

class Node(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):  
        self.head = None

    def insertNode(self, data):
        if data:
            newNode = Node(data)
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

    def reverseLL(self):
        if self.head is None or self.head.next is None:
            return self.head
        prev = None
        curr = self.head
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        self.head = prev
        
    def reverseAndPrintLL(self):
        self.reverseLL()
        self.printLL()
    
class Test (object):
    def testReverseLL(self, input, output):
        LL = LinkedList()
        LL.insertNodes(input)
        LL.reverseLL()
        assert LL.printLL() == output, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testReverseLL([1,2,3,4,5], [5,4,3,2,1])
    t.testReverseLL([1,2], [2,1])
    t.testReverseLL([],[])
    print "everything passed"
    
# O(n)
