class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        word_set = set(wordDict)
        n = len(s)
        
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        
        if not dp[n]:
            return []
        
        def backtrack(index):
            if index == 0:
                return [[]]
            sentences = []
            for i in range(index):
                if dp[i] and s[i:index] in word_set:
                    for sentence in backtrack(i):
                        sentences.append(sentence + [s[i:index]])
            return sentences
        
        sentences = backtrack(n)
        return [" ".join(sentence) for sentence in sentences]