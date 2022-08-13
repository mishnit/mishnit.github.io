# Given start and end times of all meeting-ids. find max meetings which can be accommodated in one room. return meetingids.

class Interval(object):
    def __init__(self, s=0, e=0, p=0):
        self.start = s
        self.end = e
        self.pos = p #adding position as after sorting the slots, the ids of meeting would be lost.

class Solution(object):
    def maxMeetingsInRoom(self, intervals):
        output=[]
        intervals.sort(key=lambda x: x.end)
        output.append(intervals[0].pos+1)    #add first sorted by end time meeting. Position being (i+1)
        last_end_time = intervals[0].end
        for i in range(1, len(intervals)): #check for remaining slots
            if intervals[i].start > last_end_time:
                output.append(intervals[i].pos+1) #position being (i+1)
                last_end_time = intervals[i].end
        return output   
    
class Test (object):
    def testMaxMeetingsInRoom(self, starts_at, ends_at, final_meeting_ids):
        intervals =[]
        for i in range(len(starts_at)):
            interval = Interval(starts_at[i], ends_at[i], i)
            intervals.append(interval)
        s = Solution()
        assert s.maxMeetingsInRoom(intervals)== final_meeting_ids, "Fail"
        
if __name__ == '__main__':
    t = Test()
    t.testMaxMeetingsInRoom([1,3,0,5,8,5],[2,4,6,7,9,9], [1,2,4,5])
    t.testMaxMeetingsInRoom([75250, 50074, 43659, 8931, 11273, 27545, 50879, 77924],[112960, 114515, 81825, 93424, 54316, 35533, 73383, 160252], [6,7,1])
    print "everything passed"
    
# O(n)
