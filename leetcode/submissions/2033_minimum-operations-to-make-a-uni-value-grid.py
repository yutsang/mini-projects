class Solution:
    def minOperations(self, grid: List[List[int]], x: int) -> int:
        flattened_grid = [num for row in grid for num in row]
        
        flattened_grid.sort()
        
        if any((num - flattened_grid[0]) % x != 0 for num in flattened_grid):
            return -1
        
        median = flattened_grid[len(flattened_grid) // 2]
        
        total_operations = sum(abs(num - median) // x for num in flattened_grid)
        
        return total_operations