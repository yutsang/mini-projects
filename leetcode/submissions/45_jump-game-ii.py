class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return 0
        
        jumps = 0
        current_max_reach = 0
        next_max_reach = 0
        
        for i in range(len(nums) - 1):
            next_max_reach = max(next_max_reach, i + nums[i])
            
            if i == current_max_reach:
                jumps += 1
                current_max_reach = next_max_reach
                
                if current_max_reach >= len(nums) - 1:
                    break
        
        return jumps

        