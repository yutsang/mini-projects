class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        if k == 1:
            return True

        needDecrease = 0
        dq = deque()

        for i in range(len(nums)):
            if i >= k:
                needDecrease -= dq.popleft()  # Remove the front element from the deque
            if nums[i] < needDecrease:
                return False
            decreasedNum = nums[i] - needDecrease
            dq.append(decreasedNum)
            needDecrease += decreasedNum

        return dq[-1] == 0