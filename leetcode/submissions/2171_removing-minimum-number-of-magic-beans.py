class Solution:
    def minimumRemoval(self, beans: List[int]) -> int:
        beans.sort()
        
        # Calculate the total number of beans
        total_beans = sum(beans)
        n = len(beans)
        
        # Initialize the minimum removals to a large number
        min_removals = float('inf')
        
        # Iterate over each possible target number of beans
        for i in range(n):
            # Calculate the number of beans to remove
            remove_count = total_beans - (n - i) * beans[i]
            # Update the minimum removals
            min_removals = min(min_removals, remove_count)
        
        return min_removals