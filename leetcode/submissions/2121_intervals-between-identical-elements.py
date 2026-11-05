class Solution:
    def getDistances(self, arr: List[int]) -> List[int]:
        n = len(arr)
        ans = [0] * n
        prefix = [0] * n
        suffix = [0] * n
        numToIndices = defaultdict(list)

        for i in range(n):
            numToIndices[arr[i]].append(i)

        for indices in numToIndices.values():
            for i in range(1, len(indices)):
                currIndex = indices[i]
                prevIndex = indices[i - 1]
                prefix[currIndex] += prefix[prevIndex] + i * (currIndex - prevIndex)
            for i in range(len(indices) - 2, -1, -1):
                currIndex = indices[i]
                prevIndex = indices[i + 1]
                suffix[currIndex] += suffix[prevIndex] + (len(indices) - i - 1) * (prevIndex - currIndex)

        for i in range(n):
            ans[i] = prefix[i] + suffix[i]

        return ans