class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows, cols = len(board), len(board[0])
        
        def get_neighbors(i, j):
            directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    yield board[ni][nj] & 1
        
        for i in range(rows):
            for j in range(cols):
                live_neighbors = sum(get_neighbors(i, j))
                if board[i][j]:
                    if live_neighbors in (2, 3):
                        board[i][j] = 3  # Live cell becomes live
                else:
                    if live_neighbors == 3:
                        board[i][j] = 2  # Dead cell becomes live
        
        for i in range(rows):
            for j in range(cols):
                board[i][j] >>= 1  # Update the board with the new states