class Solution:
    def minDeletions(self, s: str) -> int:
        frequency = Counter(s)
        
        frequencies = list(frequency.values())
        frequencies.sort(reverse=True)
        
        seen = set()
        deletions = 0
        
        for f in frequencies:
            while f in seen:
                deletions += 1
                f -= 1
            if f > 0:
                seen.add(f)
        
        return deletions
