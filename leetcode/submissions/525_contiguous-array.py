class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        cum_sum_map = {0: -1}
        max_length = 0
        cum_sum = 0
    
        for i, num in enumerate(nums):
            cum_sum += 1 if num == 1 else -1
        
            if cum_sum in cum_sum_map:
                max_length = max(max_length, i - cum_sum_map[cum_sum])
            else:
                cum_sum_map[cum_sum] = i
    
        return max_length    