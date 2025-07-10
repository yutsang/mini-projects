class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            if s[right] in char_index_map:
                # Move the left pointer to the right of the last occurrence of s[right]
                left = max(left, char_index_map[s[right]] + 1)
            
            # Update the last index of the character
            char_index_map[s[right]] = right
            
            # Update the maximum length of the substring
            max_length = max(max_length, right - left + 1)
        
        return max_length