class Solution:
    def minFlips(self, s: str) -> int:
        n = len(s)
        s_extended = s + s
        
        pattern1 = ''.join(['01'[(i % 2)] for i in range(2 * n)])
        pattern2 = ''.join(['10'[(i % 2)] for i in range(2 * n)])
        
        flips1 = sum(s_extended[i] != pattern1[i] for i in range(n))
        flips2 = sum(s_extended[i] != pattern2[i] for i in range(n))
        
        min_flips = min(flips1, flips2)
        
        for i in range(n):
            if s_extended[i] != pattern1[i]:
                flips1 -= 1
            if s_extended[i] != pattern2[i]:
                flips2 -= 1
            
            if s_extended[i + n] != pattern1[i + n]:
                flips1 += 1
            if s_extended[i + n] != pattern2[i + n]:
                flips2 += 1
            
            min_flips = min(min_flips, flips1, flips2)
        
        return min_flips