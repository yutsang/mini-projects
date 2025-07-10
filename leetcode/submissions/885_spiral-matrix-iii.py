class Solution:
    def spiralMatrixIII(self, rows: int, cols: int, rStart: int, cStart: int) -> List[List[int]]:
        # Directions for right, down, left, and up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        steps = 0
        direction_index = 0
        
        # Total number of cells to visit
        total_cells = rows * cols
        
        while len(result) < total_cells:
            # Increase steps every two directions
            if direction_index % 2 == 0:
                steps += 1
            
            # Move in the current direction 'steps' times
            for _ in range(steps):
                # Calculate the current position
                if 0 <= rStart < rows and 0 <= cStart < cols:
                    result.append([rStart, cStart])
                
                # Move to the next cell in the current direction
                rStart += directions[direction_index][0]
                cStart += directions[direction_index][1]
            
            # Move to the next direction
            direction_index = (direction_index + 1) % 4
        
        return result