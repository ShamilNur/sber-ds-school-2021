import pytest
import numpy as np

from hw1.leetcode.maximum_subarray import max_sub_array


class Generator:
    def __init__(self, start=0, finish=5):
        self.start = start
        self.finish = finish

    def __call__(self):
        return np.arange(self.start, self.finish)


@pytest.fixture
def positive_number():
    numbers = np.random.randint(low=1, high=100, size=4)
    return numbers


@pytest.fixture
def negative_number():
    return np.random.randint(low=-10000, high=10000, size=5)


def test_positive_number(positive_number):
    assert max_sub_array(positive_number) > 0


def test_negative_number(negative_number):
    assert max_sub_array(negative_number) < 0
