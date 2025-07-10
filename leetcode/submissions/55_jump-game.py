class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0
        
        for index, jump_length in enumerate(nums):
            if max_reach < index:
                return False
            max_reach = max(max_reach, index + jump_length)
        
        return True