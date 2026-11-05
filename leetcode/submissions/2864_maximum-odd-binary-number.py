class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        count1 = s.count('1')
    
        result = '1' * (count1 - 1) + '0' * (len(s) - count1) + '1'
        return result
        