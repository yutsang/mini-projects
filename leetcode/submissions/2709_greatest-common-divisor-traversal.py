class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

class Solution:
    @staticmethod
    def canTraverseAllPairs(nums: List[int]) -> bool:
        if len(nums) == 1:
            return True  
        
        count = len(nums)
        nums = list(set(nums)) 

        if count > 1 and 1 in nums:
            return False
        
        n = len(nums)
        uf = UnionFind(n)
        
        factor_index = {}
        
        for i, num in enumerate(nums):
            f = 2
            while f * f <= num:
                if num % f == 0:
                    if f in factor_index:
                        uf.union(i, factor_index[f])
                    else:
                        factor_index[f] = i
                    while num % f == 0:
                        num //= f
                f += 1
            if num > 1:
                if num in factor_index:
                    uf.union(i, factor_index[num])
                else:
                    factor_index[num] = i
        
        root = uf.find(0)
        for i in range(1, n):
            if uf.find(i) != root:
                return False
        
        return True