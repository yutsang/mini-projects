class Solution:
    def countTriples(self, n: int) -> int:
        count = 0
        for c in range(1, n + 1):
            for a in range(1, c + 1):
                b_squared = c**2 - a**2
                if b_squared > 0:
                    b = int(b_squared**0.5)
                    if b**2 == b_squared and b <= n:
                        count += 1
        return count
        