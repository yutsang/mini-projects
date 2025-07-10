class Solution:
    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        if not envelopes:
            return 0
        
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        
        dp = []
        
        for width, height in envelopes:
            left, right = 0, len(dp)
            
            while left < right:
                mid = (left + right) // 2
                if dp[mid][1] < height:
                    left = mid + 1
                else:
                    right = mid
            
            if left == len(dp):
                dp.append([width, height])
            elif dp[left][1] > height:
                dp[left] = [width, height]
        
        return len(dp)