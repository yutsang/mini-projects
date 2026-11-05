class Solution:
    def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
        n = len(jobDifficulty)
        
        if n < d:
            return -1
        
        dp = [[float('inf')] * d for _ in range(n)]
        
        dp[0][0] = jobDifficulty[0]
        for i in range(1, n):
            dp[i][0] = max(dp[i-1][0], jobDifficulty[i])
        
        for i in range(1, n):
            for j in range(1, min(i+1, d)):
                max_difficulty = 0
                for k in range(i, j-1, -1):
                    max_difficulty = max(max_difficulty, jobDifficulty[k])
                    dp[i][j] = min(dp[i][j], dp[k-1][j-1] + max_difficulty)
        
        return dp[n-1][d-1] if dp[n-1][d-1] != float('inf') else -1