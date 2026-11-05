class Solution:
    def firstCompleteIndex(self, arr: List[int], mat: List[List[int]]) -> int:
        position = {}
        m, n = len(mat), len(mat[0])
        for r in range(m):
            for c in range(n):
                position[mat[r][c]] = (r, c)
        
        row_count = [0] * m
        col_count = [0] * n
        
        for index, value in enumerate(arr):
            if value in position:
                r, c = position[value]
                row_count[r] += 1
                col_count[c] += 1

                if row_count[r] == n or col_count[c] == m:
                    return index
        
        return -1