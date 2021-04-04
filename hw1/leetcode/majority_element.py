from typing import List


def majority_element(self, nums: List[int]) -> int:
    freq = {}
    n = len(nums)
    for x in nums:
        count = freq.get(x, 0) + 1
        freq[x] = count

        if count > n / 2:
            return x
