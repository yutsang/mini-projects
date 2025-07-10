class Solution:
    def minJumps(self, arr: List[int]) -> int:
        if len(arr) == 1:
            return 0
        
        graph = defaultdict(list)
        for i, value in enumerate(arr):
            graph[value].append(i)
        
        queue = deque([(0, 0)])  
        visited = set([0])
        
        while queue:
            index, steps = queue.popleft()
            
            if index == len(arr) - 1:
                return steps
            
            if index + 1 < len(arr) and index + 1 not in visited:
                visited.add(index + 1)
                queue.append((index + 1, steps + 1))
            
            if index - 1 >= 0 and index - 1 not in visited:
                visited.add(index - 1)
                queue.append((index - 1, steps + 1))
            
            while graph[arr[index]]:
                next_index = graph[arr[index]].pop()
                if next_index not in visited:
                    visited.add(next_index)
                    queue.append((next_index, steps + 1))
        
        return -1  
        