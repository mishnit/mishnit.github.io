'''
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.
'''

class MinStack(object):

    def __init__(self):
        self.stack = []
        self.min = sys.maxint
        

    def push(self, x):
        if x <= self.min:
            self.stack.append(self.min)
            self.min = x
        self.stack.append(x)

    def pop(self):
        if self.stack.pop() == self.min:
            self.min = self.stack.pop()

    def top(self):
        return self.stack[-1]
        

    def getMin(self):
        return self.min
