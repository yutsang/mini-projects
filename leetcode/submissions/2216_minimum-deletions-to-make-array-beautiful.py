class Solution:
    def minDeletion(self, nums: List[int]) -> int:
        deletions = 0
        i = 0
        n = len(nums)
        
        while i < n - 1:
            if nums[i] == nums[i + 1]:
                deletions += 1
            else:
                i += 1  
            i += 1  
        
        if (n - deletions) % 2 != 0:
            deletions += 1
        
        return deletions