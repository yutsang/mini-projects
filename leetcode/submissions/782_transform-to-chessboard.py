class Solution:
    def movesToChessboard(self, board: List[List[int]]) -> int:
        n = len(board)
        
        def can_form_chessboard():
            row_sum = sum(board[0])
            col_sum = sum(board[i][0] for i in range(n))
            row_pattern = board[0]
            col_pattern = [board[i][0] for i in range(n)]
            
            if not (n // 2 <= row_sum <= (n + 1) // 2) or not (n // 2 <= col_sum <= (n + 1) // 2):
                return False
            
            for i in range(n):
                if board[i] != row_pattern and board[i] != [1 - x for x in row_pattern]:
                    return False
                if [board[j][i] for j in range(n)] != col_pattern and [board[j][i] for j in range(n)] != [1 - x for x in col_pattern]:
                    return False
                
            return True
        
        if not can_form_chessboard():
            return -1
        
        def min_swaps(line):
            swaps1 = swaps2 = 0
            for i in range(n):
                if line[i] != i % 2:
                    swaps1 += 1
                if line[i] != (i + 1) % 2:
                    swaps2 += 1
            if n % 2 == 0:
                return min(swaps1, swaps2) // 2
            else:
                return swaps1 // 2 if swaps1 % 2 == 0 else swaps2 // 2
        
        row_swaps = min_swaps(board[0])
        col_swaps = min_swaps([board[i][0] for i in range(n)])
        
        return row_swaps + col_swaps