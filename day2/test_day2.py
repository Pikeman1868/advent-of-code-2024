import pytest
from typing import List

from day2 import *


@pytest.fixture
def input_file() -> str:
    return """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

@pytest.fixture
def input(input_file:str) -> List[str]:
    return input_file.splitlines()

@pytest.fixture
def safe_decreasing():
    return [7, 6, 4, 2, 1]

@pytest.fixture
def unsafe_decrease():
    return [1, 2, 7, 8, 9]

@pytest.fixture
def unsafe_large_increase():
    return [1, 2, 7, 8, 9]

@pytest.fixture
def unsafe_large_decrease():
    return [9, 7, 6, 2, 1]

@pytest.fixture
def unsafe_variable_direction():
    return [1, 3, 2, 4, 5]

@pytest.fixture
def unsafe_neither_increase_nor_decrease():
    return  [8, 6, 4, 4, 1]

@pytest.fixture
def safe_increase():
    return [1, 3, 6, 7, 9]

def test_part1(input_file):
    assert count_safe_reactor_days(input_file) == 2

def test_parsing_data(input_file):
    assert parse_reactor_data(input_file) == [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]


@pytest.mark.parametrize("input, expected", [([7, 6, 4, 2, 1], True), ([1, 2, 7, 8, 9], False ),
    ([1, 2, 7, 8, 9], False), ([9, 7, 6, 2, 1], False), ([1, 3, 2, 4, 5], False), ([8, 6, 4, 4, 1], False), ([1, 3, 6, 7, 9], True)])
def test_read_day(input, expected):
    assert is_day_safe(input) == expected

@pytest.mark.parametrize("input, expected", [([7, 6, 4, 2, 1], DecreasingValidator), ([1, 2, 7, 8, 9], IncreasingValidator ), ([9, 7, 6, 2, 1], DecreasingValidator), ([1, 3, 2, 4, 5], IncreasingValidator), ([8, 6, 4, 4, 1], DecreasingValidator), ([1, 3, 6, 7, 9], IncreasingValidator)])
def test_determine_direction(input, expected):
    isinstance(determine_direction(input), expected)
