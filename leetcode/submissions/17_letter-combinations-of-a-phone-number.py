class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        mapping = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
        }
        
        if not digits:
            return []
        
        def backtrack(index, path):
            if index == len(digits):
                combinations.append(''.join(path))
                return
            
            for letter in mapping[digits[index]]:
                backtrack(index + 1, path + [letter])
        
        combinations = []
        backtrack(0, [])
        return combinations