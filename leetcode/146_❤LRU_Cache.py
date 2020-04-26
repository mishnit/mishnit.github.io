class LRUCache:
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.cache = {}
        self.queue = []

    def updateQueue(self, key):
        self.queue.remove(key)
        self.queue.insert(0, key)

    def get(self, key):
        """
        :rtype: int
        """
        if key in self.cache:
            self.updateQueue(key)
            return self.cache[key]
        else:
            return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: nothing
        """
        if not key or not value:
            return None
        if key in self.cache:
            self.queue.remove(key)
        elif len(self.queue) == self.capacity:
            del self.cache[self.queue.pop(-1)]

        self.cache[key] = value
        self.queue.insert(0, key)

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
