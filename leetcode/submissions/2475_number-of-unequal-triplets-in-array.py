class Solution:
    def unequalTriplets(self, nums: List[int]) -> int:
        counter = Counter(nums)
        distinct_elements = list(counter.keys())
        total_triplets = 0

        distinct_count = len(distinct_elements)
        for i in range(distinct_count):
            for j in range(i + 1, distinct_count):
                for k in range(j + 1, distinct_count):
                    total_triplets += counter[distinct_elements[i]] * counter[distinct_elements[j]] * counter[distinct_elements[k]]

        return total_triplets