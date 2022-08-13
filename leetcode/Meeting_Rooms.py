# Given meeting intervals check if one can attend all the meetings?

class Interval(object):
    def __init__(self, s=0, e=0):
        self.start = s
        self.end = e

class Solution(object):
    def canAttendMeetings(self, intervals):
        intervals.sort(key=lambda x: x.start)
        for i in range(len(intervals) - 1):
            if intervals[i].end > intervals[i + 1].start:
                return False
        return True     
    
class Test (object):
    def testCanAttendMeetings(self, slots, output):
        intervals =[]
        for slot in slots:
            interval = Interval(slot[0], slot[1])
            intervals.append(interval)
        s = Solution()
        assert s.canAttendMeetings(intervals)== output, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testCanAttendMeetings([[0,20],[5,10],[20,30]], False)
    t.testCanAttendMeetings([[4,6],[7,10]], True)
    print "everything passed"
    
# O(n)
