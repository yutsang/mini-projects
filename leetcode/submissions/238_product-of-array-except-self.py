class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        if n == 0:
            return []
    
        prefix_products = [1] * n
        suffix_products = [1] * n
        result = [1] * n
    
        for i in range(1, n):
            prefix_products[i] = prefix_products[i - 1] * nums[i - 1]
    
        for i in range(n - 2, -1, -1):
            suffix_products[i] = suffix_products[i + 1] * nums[i + 1]
    
        for i in range(n):
            result[i] = prefix_products[i] * suffix_products[i]
    
        return result    