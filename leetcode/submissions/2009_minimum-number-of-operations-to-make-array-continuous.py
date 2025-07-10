class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        nums = sorted(set(nums))  
        
        max_length = 0
        right = 0
        
        for left in range(len(nums)):
            while right < len(nums) and nums[right] < nums[left] + n:
                right += 1
            max_length = max(max_length, right - left)
        
        return n - max_length