class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        INF = 10000000000000000

        # Initialize the prefix sum array
        sum_vals = [0] * (n + 1)
        f = [-INF] * (k + 1)
        g = [-INF] * (k + 1)
        g[0] = 0  # Base case

        for i in range(1, n + 1):
            f[0] = 0  # Reset f[0] for each i
            sum_vals[i] = sum_vals[i - 1] + nums[i - 1]  # Calculate prefix sum

            for j in range(1, k + 1):
                t = (1 if j % 2 == 1 else -1) * sum_vals[i] * (k - j + 1)

                f[j] = max(f[j], g[j - 1] + t)
                g[j - 1] = max(g[j - 1], f[j - 1] - t)

        return f[k]