class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Negative numbers are not palindromes
        if x < 0:
            return False
        
        # Store the original number
        original = x
        reversed_num = 0
        
        # Reverse the number
        while x > 0:
            digit = x % 10
            reversed_num = reversed_num * 10 + digit
            x //= 10
        
        # Compare the reversed number with the original
        return original == reversed_num