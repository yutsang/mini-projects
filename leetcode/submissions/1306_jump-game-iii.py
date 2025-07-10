class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        visited = set()
        queue = deque([start])

        while queue:
            index = queue.popleft()
            if arr[index] == 0:
                return True
            visited.add(index)
            for jump in [index + arr[index], index - arr[index]]:
                if 0 <= jump < n and jump not in visited:
                    queue.append(jump)

        return False    