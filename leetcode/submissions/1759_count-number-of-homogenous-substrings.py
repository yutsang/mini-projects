class Solution:
    def countHomogenous(self, s: str) -> int:
        mod = 10**9 + 7
        count = 0
        current_length = 1

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                current_length += 1
            else:
                count = (count + (current_length * (current_length + 1)) // 2) % mod
                current_length = 1

        count = (count + (current_length * (current_length + 1)) // 2) % mod
        return count