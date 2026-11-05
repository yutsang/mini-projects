class Solution:
    def checkValid(self, matrix: List[List[int]]) -> bool:
        n = len(matrix)
        
        def check_rows(matrix):
            for row in matrix:
                if sorted(row) != list(range(1, n + 1)):
                    return False
            return True

        def check_columns(matrix):
            for col in range(n):
                if sorted(matrix[row][col] for row in range(n)) != list(range(1, n + 1)):
                    return False
            return True
        
        return check_rows(matrix) and check_columns(matrix)