class Solution:
    def spiralMatrix(self, m: int, n: int, head: Optional[ListNode]) -> List[List[int]]:
        matrix = [[-1] * n for _ in range(m)]  # Initialize the matrix with -1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        row, col = 0, 0  # Start position
        direction_index = 0  # Start facing 'right'

        while head:
            matrix[row][col] = head.val  # Fill the value in the matrix
            head = head.next  # Move to the next node in the linked list

            # Calculate the next position
            next_row = row + directions[direction_index][0]
            next_col = col + directions[direction_index][1]

            # Check if the next position is within bounds and not yet filled
            if 0 <= next_row < m and 0 <= next_col < n and matrix[next_row][next_col] == -1:
                row, col = next_row, next_col  # Move to the next position
            else:
                # Change direction clockwise
                direction_index = (direction_index + 1) % 4
                row += directions[direction_index][0]
                col += directions[direction_index][1]

        return matrix