class Solution:
    def minimumOperations(self, nums: List[int], start: int, goal: int) -> int:
        # Initialize a seen list to track visited numbers
        seen = [0] * 1001
        q = deque([start])  # Initialize the queue with the starting number

        # BFS to find the minimum operations
        for ans in range(1, 10000):  # Arbitrarily large number to limit the loop
            for _ in range(len(q)):
                x = q.popleft()
                
                # Check all operations
                for n in nums:
                    for t in (x + n, x - n, x ^ n):
                        if t == goal:
                            return ans  # Return the number of operations if we reach the goal
                        if 0 <= t <= 1000 and not seen[t]:  # Only consider valid numbers
                            seen[t] = 1  # Mark this number as seen
                            q.append(t)  # Add the new number to the queue

        return -1