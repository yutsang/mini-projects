class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_pairs = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in '({[':
                stack.append(char)
            elif char in ')}]':
                if not stack or stack.pop() != bracket_pairs[char]:
                    return False
        
        return len(stack) == 0