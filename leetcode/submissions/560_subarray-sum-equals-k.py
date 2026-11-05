class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        cumulative_sum = 0
        sum_map = defaultdict(int)
        sum_map[0] = 1  
        for num in nums:
            cumulative_sum += num
            if cumulative_sum - k in sum_map:
                count += sum_map[cumulative_sum - k]
            sum_map[cumulative_sum] += 1

        return count