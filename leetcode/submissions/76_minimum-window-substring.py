from collections import Counter, defaultdict

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        dict_t = Counter(t)
        required = len(dict_t)
        l, r = 0, 0  
        formed = 0  
        window_counts = defaultdict(int)
        min_length = float("inf")
        min_window = (0, 0)

        # Sliding window
        while r < len(s):
            character = s[r]
            window_counts[character] += 1

            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            while l <= r and formed == required:
                character = s[l]

                if r - l + 1 < min_length:
                    min_length = r - l + 1
                    min_window = (l, r)

                window_counts[character] -= 1
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1

                l += 1

            r += 1

        return s[min_window[0]:min_window[1] + 1] if min_length != float("inf") else ""