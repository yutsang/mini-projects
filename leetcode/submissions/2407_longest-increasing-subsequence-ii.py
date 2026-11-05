
class Solution:
    def lengthOfLIS(self, nums: List[int], k: int) -> int:
        n = max(nums)
        dp = [0] * (2 * (n + 1))
        
        def query(l: int, r: int) -> int:
            ans = 0
            l += n
            r += n
            while l < r:
                if l & 1:
                    ans = max(ans, dp[l])
                    l += 1
                if r & 1:
                    r -= 1
                    ans = max(ans, dp[r])
                l >>= 1
                r >>= 1
            return ans
        
        def update(i: int, val: int) -> None:
            dp[i + n] = val
            i += n
            while i > 1:
                i >>= 1
                dp[i] = max(dp[i * 2], dp[i * 2 + 1])
        
        ans = 0
        for x in nums:
            cur = 1 + query(max(1, x - k), x)
            update(x, cur)
            ans = max(ans, cur)
        
        return ans