# https://leetcode.com/problems/water-bottles/

class Solution(object):
    def numWaterBottles(self, numBottles, numExchange):
        drink = numBottles
        bottle = numBottles
        while bottle >= numExchange:
            drink = drink + bottle/numExchange
            bottle = (bottle/numExchange) + (bottle%numExchange)
        return drink
