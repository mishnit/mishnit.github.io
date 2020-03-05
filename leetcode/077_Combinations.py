class Solution(object):
        def combinations(self, n,k,ind,ans,res):
            if k == 0:
                res.append(ans[:])
                return
            for i in range(ind,n-k+2):
                ans.append(i)
                self.combinations(n,k-1,i+1,ans,res)
                ans.pop()
        
        def combine(self, n, k):
            res = []
            self.combinations(n,k,1,[],res)
            return res
    
if __name__ == "__main__":
    s = Solution()
    print s.combine(4, 2)
