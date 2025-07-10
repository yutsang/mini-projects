class Solution:
    def customSortString(self, order: str, s: str) -> str:
        priority = {char: i for i, char in enumerate(order)}
    
        sorted_s = sorted(s, key=lambda char: priority.get(char, len(order)))
    
        return ''.join(sorted_s)    