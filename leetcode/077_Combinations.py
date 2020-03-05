class Solution(object):
    def combine(self, n, k):
        def combinations(n,k,ind,ans,res):
            if k == 0:
                res.append(ans[:])
                return
            for i in range(ind,n-k+2):
                ans.append(i)
                combinations(n,k-1,i+1,ans,res)
                ans.pop()
        res = []
        combinations(n,k,1,[],res)
        return res
    
if __name__ == "__main__":
    s = Solution()
    print s.combine(4, 2)
