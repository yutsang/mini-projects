class Solution:
    def luckyNumbers (self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
    
        min_row_values = [min(row) for row in matrix]
    
        max_col_values = [max(matrix[i][j] for i in range(m)) for j in range(n)]
    
        lucky_numbers = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == min_row_values[i] and matrix[i][j] == max_col_values[j]:
                    lucky_numbers.append(matrix[i][j])
    
        return lucky_numbers