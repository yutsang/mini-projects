class Solution:
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        max_score = sum(cardPoints[:k])
        current_sum = max_score

        for i in range(k):
            current_sum -= cardPoints[k - 1 - i]  
            current_sum += cardPoints[n - 1 - i] 
            max_score = max(max_score, current_sum)

        return max_score
