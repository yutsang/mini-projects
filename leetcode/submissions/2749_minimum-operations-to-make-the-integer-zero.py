class Solution:
  def makeTheIntegerZero(self, num1: int, num2: int) -> int:

    for ops in range(61):
      target = num1 - ops * num2
      if target.bit_count() <= ops <= target:
        return ops

    return -1