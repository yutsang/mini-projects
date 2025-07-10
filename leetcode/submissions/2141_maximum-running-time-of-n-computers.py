class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        def can_run(T):
            total_power = 0
            for b in batteries:
                total_power += min(b, T)
            return total_power >= n * T

        left, right = 0, sum(batteries) // n
        while left < right:
            mid = (left + right + 1) // 2
            if can_run(mid):
                left = mid
            else:
                right = mid - 1
        
        return left