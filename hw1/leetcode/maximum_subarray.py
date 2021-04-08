from typing import List


def max_sub_array(nums: List[int]) -> int:
    max_sub = nums[0]
    part_sum = 0
    for x in nums:
        part_sum = max(part_sum + x, x)
        max_sub = max(max_sub, part_sum)

    return max_sub
