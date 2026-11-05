class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        min_index = nums.index(min(nums))
        max_index = nums.index(max(nums))
        
        n = len(nums)
        
        front_removal = max(min_index, max_index) + 1
        
        back_removal = n - min(min_index, max_index)
        
        removal_both_sides = min(min_index, max_index) + 1 + (n - max(min_index, max_index))
        
        min_deletions = min(front_removal, back_removal, removal_both_sides)
        
        return min_deletions