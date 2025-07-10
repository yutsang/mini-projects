class Solution:
    def checkZeroOnes(self, s: str) -> bool:
        max_ones = 0
        max_zeros = 0
        current_count = 0
        
        # Iterate through the string to count segments
        for char in s:
            if char == '1':
                current_count += 1
            else:
                max_ones = max(max_ones, current_count)
                current_count = 0
        max_ones = max(max_ones, current_count)
        
        current_count = 0
        for char in s:
            if char == '0':
                current_count += 1
            else:
                max_zeros = max(max_zeros, current_count)
                current_count = 0
        max_zeros = max(max_zeros, current_count)
        
        return max_ones > max_zeros