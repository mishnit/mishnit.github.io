# Given stock prices, return max profit by doing buy/sell transactions.
# Tip: choose two prices such that price at later date minus price at older date is maximised

class Solution(object):
    def maxProfit(self, prices):
        if len(prices) == 0:
            return 0
        
        maxprofit = 0
        l = 0
        for r in range(1, len(prices)):
            if prices[r] < prices[l]:
                l = r
            maxprofit = max(maxprofit, prices[r] - prices[l])
        return maxprofit
        
    
class Test (object):
    def testMaxProfit(self):
        s = Solution()
        assert s.maxProfit([7,1,5,3,6,4]) == 5, "Fail"
        assert s.maxProfit([7,6,4,3,1]) == 0, "Fail"
        print "everything passed"
        
if __name__ == '__main__':
    t = Test()
    t.testMaxProfit()

# O(n)
