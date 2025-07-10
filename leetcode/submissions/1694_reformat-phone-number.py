class Solution:
    def reformatNumber(self, number: str) -> str:
        # Step 1: Remove spaces and dashes
        digits = ''.join(filter(str.isdigit, number))
        
        # Step 2: Initialize an empty list to hold the formatted blocks
        blocks = []
        
        # Step 3: Process the digits into blocks
        i = 0
        while i < len(digits):
            # If there are 4 or more digits left
            if len(digits) - i > 4:
                blocks.append(digits[i:i+3])  # Take 3 digits
                i += 3
            else:
                # Handle the last 4 or fewer digits
                remaining = len(digits) - i
                if remaining == 4:
                    blocks.append(digits[i:i+2])  # First 2 digits
                    blocks.append(digits[i+2:i+4])  # Next 2 digits
                else:
                    blocks.append(digits[i:i+remaining])  # Take the remaining digits
                break
        
        # Step 4: Join the blocks with dashes
        return '-'.join(blocks)