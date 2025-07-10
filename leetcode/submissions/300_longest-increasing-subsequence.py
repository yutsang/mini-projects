class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = []  
        for num in nums:
            pos = bisect.bisect_left(dp, num)
            if pos == len(dp):
                dp.append(num)
            else:
                dp[pos] = num  

        return len(dp)