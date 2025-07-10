class Solution:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        count = 0
        prefix_sum = 0
        sum_count = defaultdict(int)
        sum_count[0] = 1 
        
        for num in nums:
            prefix_sum += num
            count += sum_count[prefix_sum - goal]
            sum_count[prefix_sum] += 1
        
        return count