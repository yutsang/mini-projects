class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        # Constants for 32-bit signed integer range
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # Handle edge cases
        if divisor == 0:
            raise ValueError("Divisor cannot be zero")
        if dividend == 0:
            return 0
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX
        
        # Determine the sign of the result
        negative = (dividend < 0) != (divisor < 0)
        
        # Work with positive values
        dividend = abs(dividend)
        divisor = abs(divisor)
        
        # Initialize the quotient
        quotient = 0
        
        # Use bit shifting to find the quotient
        while dividend >= divisor:
            temp_divisor = divisor
            multiple = 1
            while dividend >= (temp_divisor << 1):
                temp_divisor <<= 1
                multiple <<= 1
            dividend -= temp_divisor
            quotient += multiple
        
        # Apply the sign to the result
        if negative:
            quotient = -quotient
        
        # Clamp the result to the 32-bit signed integer range
        return max(INT_MIN, min(INT_MAX, quotient))
