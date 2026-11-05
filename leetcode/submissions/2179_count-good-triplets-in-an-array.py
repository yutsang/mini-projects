class Solution:
    def goodTriplets(self, A: List[int], B: List[int]) -> int:
        N = len(A)
        ans = 0
        m = [0] * N
        lt = [0] * N
        tmp = [0] * N
        tmpLt = [0] * N
        index = [0] * N
        
        # Step 1: Map indices of A
        for i in range(N):
            m[A[i]] = i
        
        # Step 2: Modify B to reflect positions in A and fill index
        for i in range(N):
            B[i] = m[B[i]]
            index[B[i]] = i
        
        # Step 3: Merge function for counting
        def merge(begin: int, end: int) -> None:
            if begin + 1 >= end:
                return
            mid = (begin + end) // 2
            merge(begin, mid)
            merge(mid, end)
            i, j, k = begin, mid, begin
            for k in range(begin, end):
                if j >= end or (i < mid and B[i] < B[j]):
                    tmp[k] = B[i]
                    tmpLt[k] = lt[i]
                    i += 1
                else:
                    tmp[k] = B[j]
                    tmpLt[k] = tmpLt[j] + (i - begin)
                    j += 1
            for i in range(begin, end):
                B[i] = tmp[i]
                lt[i] = tmpLt[i]
        
        # Step 4: Perform merge sort and count
        merge(0, N)
        
        # Step 5: Calculate the number of good triplets
        for i in range(N):
            ans += lt[i] * (N - B[i] - 1 - index[B[i]] + lt[i])
        
        return ans
