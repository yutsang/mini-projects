class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        
        prefix_sum = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            prefix_sum[i] = prefix_sum[i + 1] + piles[i]

        memo = [[-1] * (n + 1) for _ in range(n)]

        def dfs(i: int, M: int) -> int:
            if i >= n:
                return 0  
            if memo[i][M] != -1:
                return memo[i][M]

            max_stones = 0  
            for X in range(1, 2 * M + 1):
                if i + X <= n:
                    stones_taken = prefix_sum[i] - dfs(i + X, max(M, X))
                    max_stones = max(max_stones, stones_taken)

            memo[i][M] = max_stones
            return max_stones

        return dfs(0, 1) 