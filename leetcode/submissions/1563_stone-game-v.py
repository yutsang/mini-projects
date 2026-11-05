class Solution:
    def stoneGameV(self, stoneValue: List[int]) -> int:
        n = len(stoneValue)
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + stoneValue[i]

        memo = [[-1] * n for _ in range(n)]

        def dfs(i, j):
            if i == j:
                return 0
            if memo[i][j] != -1:
                return memo[i][j]

            total = prefix_sum[j + 1] - prefix_sum[i]
            max_score = 0
            for k in range(i, j):
                left_sum = prefix_sum[k + 1] - prefix_sum[i]
                right_sum = total - left_sum

                if left_sum <= right_sum:
                    max_score = max(max_score, left_sum + dfs(i, k))
                if left_sum >= right_sum:
                    max_score = max(max_score, right_sum + dfs(k + 1, j))

            memo[i][j] = max_score
            return max_score

        return dfs(0, n - 1)