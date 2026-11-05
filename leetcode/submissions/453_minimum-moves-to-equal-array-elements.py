class Solution:
    def minMoves(self, nums: List[int]) -> int:
        min_num = min(nums)
        
        moves = sum(num - min_num for num in nums)
        
        return moves