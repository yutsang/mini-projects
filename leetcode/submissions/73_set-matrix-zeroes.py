class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        if not matrix:
            return

        rows, cols = len(matrix), len(matrix[0])
        row_zero = False
        col_zero = False

        # Determine if the first row needs to be zeroed
        for j in range(cols):
            if matrix[0][j] == 0:
                row_zero = True

        # Determine if the first column needs to be zeroed
        for i in range(rows):
            if matrix[i][0] == 0:
                col_zero = True

        # Use the first row and first column to mark zeroes
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0  # Mark the first column
                    matrix[0][j] = 0  # Mark the first row

        # Zero out cells based on markers in the first row and first column
        for i in range(1, rows):
            for j in range(1, cols):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # Zero out the first row if needed
        if row_zero:
            for j in range(cols):
                matrix[0][j] = 0

        # Zero out the first column if needed
        if col_zero:
            for i in range(rows):
                matrix[i][0] = 0