class Solution:
    def maxScore(self, nums: List[int], x: int) -> int:
        n = len(nums)
        even_score = float('-inf')
        odd_score = float('-inf')
        
        if nums[0] % 2 == 0:
            even_score = nums[0]
        else:
            odd_score = nums[0]
        
        for i in range(1, n):
            if nums[i] % 2 == 0:
                even_score = max(even_score + nums[i], odd_score + nums[i] - x)
            else:
                odd_score = max(odd_score + nums[i], even_score + nums[i] - x)
        
        return max(even_score, odd_score)