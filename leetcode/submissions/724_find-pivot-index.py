class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total_sum = sum(nums)  # Step 1: Calculate the total sum
        left_sum = 0  # Initialize left sum
        
        for i in range(len(nums)):
            # Step 3: Calculate right sum
            right_sum = total_sum - left_sum - nums[i]
            
            # Step 4: Check if left sum equals right sum
            if left_sum == right_sum:
                return i  # Return the pivot index
            
            # Step 5: Update left sum for the next iteration
            left_sum += nums[i]
        
        return -1