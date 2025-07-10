class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        even_freq = Counter(nums[i] for i in range(0, len(nums), 2))
        odd_freq = Counter(nums[i] for i in range(1, len(nums), 2))

        even_most = even_freq.most_common(2) + [(None, 0)] * (2 - len(even_freq))
        odd_most = odd_freq.most_common(2) + [(None, 0)] * (2 - len(odd_freq))

        total_even = sum(even_freq.values())
        total_odd = sum(odd_freq.values())

        if even_most[0][0] != odd_most[0][0]:
            min_operations = total_even - even_most[0][1] + total_odd - odd_most[0][1]
        else:
            min_operations = min(
                total_even - even_most[0][1] + total_odd - odd_most[1][1],
                total_even - even_most[1][1] + total_odd - odd_most[0][1]
            )

        return min_operations