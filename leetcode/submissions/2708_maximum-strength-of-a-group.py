class Solution:
    def maxStrength(self, nums: List[int]) -> int:
        if len(nums) == 1:  # Only one number
            return nums[0]
        
        if len(nums) == 2:  # Two numbers
            if nums[0]*nums[1] > 0:
                return nums[0] * nums[1]
            else:
                return max(nums[0], nums[1])
        
        positives = []
        negatives = []
        zero_count = 0
        
        for num in nums:
            if num > 0:
                positives.append(num)
            elif num < 0:
                negatives.append(num)
            else:
                zero_count += 1

        positive_product = 1
        for p in positives:
            positive_product *= p
                    
        negative_count = len(negatives)
        
        if negative_count % 2 == 1:  # Odd number of negatives
            negatives.remove(max(negatives))  # Remove the largest negative
                    
        negative_product = 1
        for n in negatives:
            negative_product *= n
                    
        if positive_product == 1 and not positives and zero_count > 0 and not negatives:  # All zeros
            print("exit here")
            return 0
        
        if not positives and negative_count > 0:  # Only negative numbers
            return negative_product
                
        return positive_product * negative_product