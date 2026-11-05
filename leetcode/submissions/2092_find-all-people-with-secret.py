class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        # Method implementation
        secret_holders = set([0, firstPerson])
    
        meetings.sort(key=lambda x: x[2])
    
        for time, group in groupby(meetings, key=lambda x: x[2]):
            graph = defaultdict(set)
            for x, y, _ in group:
                graph[x].add(y)
                graph[y].add(x)
        
            queue = deque([person for person in graph if person in secret_holders])
            visited = set(queue)
        
            while queue:
                person = queue.popleft()
                for contact in graph[person]:
                    if contact not in secret_holders:
                        secret_holders.add(contact)
                    if contact not in visited:
                        visited.add(contact)
                        queue.append(contact)
    
        return list(secret_holders)
        