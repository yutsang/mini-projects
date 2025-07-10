class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        n = len(nums)
        dp = [-1] * n
        dp[0] = 0  

        for j in range(1, n):
            for i in range(j):
                if abs(nums[j] - nums[i]) <= target and dp[i] != -1:
                    dp[j] = max(dp[j], dp[i] + 1)

        return dp[n-1]
