class Solution:
    def reverse(self, x: int) -> int:
        INT_MIN, INT_MAX = -2**31, 2**31 - 1

        sign = -1 if x < 0 else 1
        x *= sign

        reversed_x = 0
        while x != 0:
            reversed_x = reversed_x * 10 + x % 10
            x //= 10

        reversed_x *= sign

        if reversed_x < INT_MIN or reversed_x > INT_MAX:
            return 0
        return reversed_x