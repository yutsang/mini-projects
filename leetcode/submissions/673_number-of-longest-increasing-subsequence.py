class Solution:
    def findNumberOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0

        lengths = [1] * n 
        counts = [1] * n  

        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:  
                    if lengths[i] < lengths[j] + 1:
                        lengths[i] = lengths[j] + 1
                        counts[i] = counts[j]  
                    elif lengths[i] == lengths[j] + 1:
                        counts[i] += counts[j]  

        max_length = max(lengths)
        return sum(c for l, c in zip(lengths, counts) if l == max_length)