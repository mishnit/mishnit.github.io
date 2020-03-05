# class Solution(object):
#     def isPalindrome(self, x):
#         """
#         :type x: int
#         :rtype: bool
#         """

class Solution(object):
    def isPalindrome(self, x):
        if x < 0:
            return False
        ls = 0
        tmp = x
        while tmp != 0:
            ls += 1
            tmp = tmp // 10
        tmp = x
        for i in range(ls/2):
            right = tmp % 10
            left = tmp / (10 ** (ls - 2 * i - 1))
            left = left % 10
            # print left, right
            if left != right:
                return False
            tmp = tmp // 10
        return True


    # def isPalindrome(self, x):
    #     #leetcode book
    #     if x < 0:
    #         return False
    #     div = 1
    #     while x / div >= 10:
    #         div *= 10
    #     while x != 0:
    #         left = x / div
    #         right = x % 10
    #         if left != right:
    #             return False
    #         x = (x % div) / 10
    #         div /= 100
    #     return True


    # def isPalindrome(self, x):
    #     # reverse number
    #     if x < 0:
    #         return False
    #     rev_x = 0
    #     temp = x
    #     while temp != 0:
    #         curr = temp % 10
    #         rev_x = rev_x * 10 + curr
    #         temp = temp // 10
    #     if rev_x == x:
    #         return True
    #     else:
    #         return False


if __name__ == '__main__':
    # begin
    s = Solution()
    print s.isPalindrome(1001)