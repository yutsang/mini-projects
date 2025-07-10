class Solution:
    def isPalindrome(self, s: str) -> bool:
        normalized_str = ''.join(char.lower() for char in s if char.isalnum())
        
        return normalized_str == normalized_str[::-1]