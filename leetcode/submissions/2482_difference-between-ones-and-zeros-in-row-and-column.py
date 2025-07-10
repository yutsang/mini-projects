class Solution:
    def onesMinusZeros(self, grid: List[List[int]]) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        
        onesRow = [0] * m
        zerosRow = [0] * m
        for i in range(m):
            onesRow[i] = sum(grid[i])
            zerosRow[i] = n - onesRow[i]
        
        onesCol = [0] * n
        zerosCol = [0] * n
        for j in range(n):
            for i in range(m):
                if grid[i][j] == 1:
                    onesCol[j] += 1
                else:
                    zerosCol[j] += 1
        
        diff = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                diff[i][j] = onesRow[i] + onesCol[j] - zerosRow[i] - zerosCol[j]
        
        return diff