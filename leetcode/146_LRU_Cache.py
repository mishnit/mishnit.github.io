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

    def set(self, key, value):
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

    # def __init__(self, capacity):
    #     self.dic = collections.OrderedDict()
    #     self.remain = capacity
    #
    # def get(self, key):
    #     if key not in self.dic:
    #         return -1
    #     v = self.dic.pop(key)
    #     self.dic[key] = v  # set key as the newest one
    #     return v
    #
    # def set(self, key, value):
    #     if key in self.dic:
    #         self.dic.pop(key)
    #     else:
    #         if self.remain > 0:
    #             self.remain -= 1
    #         else:  # self.dic is full
    #             self.dic.popitem(last=False)
    #     self.dic[key] = value