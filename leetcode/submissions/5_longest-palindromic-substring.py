class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""
        
        start = 0
        max_length = 1
        
        def expandAroundCenter(left: int, right: int) -> int:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1
        
        for i in range(len(s)):
            length1 = expandAroundCenter(i, i)
            if length1 > max_length:
                max_length = length1
                start = i - (length1 - 1) // 2
            
            length2 = expandAroundCenter(i, i + 1)
            if length2 > max_length:
                max_length = length2
                start = i - (length2 - 2) // 2
        
        return s[start:start + max_length]