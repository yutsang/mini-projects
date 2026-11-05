class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        n = len(s)
        queue = deque([0])
        visited = set([0])
        farthest = 0
        
        while queue:
            current = queue.popleft()
            
            start = max(current + minJump, farthest + 1)
            end = min(current + maxJump, n - 1)
            
            for next_index in range(start, end + 1):
                if next_index not in visited and s[next_index] == '0':
                    if next_index == n - 1:
                        return True
                    queue.append(next_index)
                    visited.add(next_index)
            
            farthest = end
        
        return False