# Given start and end times of all meeting-ids. find min rooms to accommodate all meetings.

class Interval(object):
    def __init__(self, s=0, e=0, p=0):
        self.start = s
        self.end = e
        self.pos = p #adding position as after sorting the slots, the ids of meeting would be lost.

class Solution(object):
    def minRooms(self, intervals):
        timeline = []
        for interval in intervals:
            timeline.append((interval.start, 1))
            timeline.append((interval.end, -1))
        timeline.sort()
        ans = curr = 0
        for _, v in timeline:
            curr += v
            ans = max(ans, curr)
        return ans   
    
class Test (object):
    def testMinRooms(self, slots, rooms):
        intervals =[]
        for slot in slots:
            interval = Interval(slot[0], slot[1])
            intervals.append(interval)
        s = Solution()
        assert s.minRooms(intervals) == rooms, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMinRooms([[0,5], [1,2], [1,10]], 3)
    t.testMinRooms([[0,5], [1,2], [6,10]], 2)
    print "everything passed"
    
# O(n)
