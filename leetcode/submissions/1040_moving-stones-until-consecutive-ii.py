class Solution:
    def numMovesStonesII(self, stones: List[int]) -> List[int]:
        n = len(stones)
        stones.sort()

        # Maximum moves: the number of gaps we can fill
        max_moves = max(stones[-1] - stones[1] - (n - 2), stones[-2] - stones[0] - (n - 2))

        # Minimum moves: check for already consecutive stones
        min_moves = n  # Start with the maximum possible moves

        j = 0
        for i in range(n):
            # Move j to maintain the window of size at most n
            while stones[i] - stones[j] + 1 > n:
                j += 1
            # Count stones in the current interval
            m = i - j + 1

            # Determine the result based on the number of stones
            if m == n - 1 and stones[i] - stones[j] == i - j:
                r = 2  # If we have n-1 stones and they are consecutive
            else:
                r = n - m  # Number of moves required to fill the gap

            min_moves = min(min_moves, r)

        return [min_moves, max_moves]