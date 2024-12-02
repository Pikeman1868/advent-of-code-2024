import pytest
from typing import List
from day1 import *


def input_file():
    return """3   4
4   3
2   5
1   3
3   9
3   3"""


@pytest.fixture
def example_read() -> List[str]:
    return ["3   4","4   3","2   5","1   3","3   9","3   3"]

@pytest.fixture
def example_pasrsed():
    return ([3,4,2,1,3,3],[4,3,5,3,9,3])

def test_part1(example_pasrsed):
    result = part_1(example_pasrsed[0], example_pasrsed[1])
    # assert result
    assert 11 == result


def test_parse_input(example_read):
    assert parse(example_read) == ([3,4,2,1,3,3],[4,3,5,3,9,3])

def test_diff_lists():
    result = diff_lists([0,1,2,3,4,5], [1,2,3,4,5,6]) 
    assert [1,1,1,1,1,1] == result


def test_part2(example_pasrsed):
    result = part2(example_pasrsed[0], example_pasrsed[1])
    assert 31 == result


def test_map_unqiue():
    result = map_unqiue([4,3,5,3,9,3])
    assert {4:1,3:3,5:1,9:1} == result


def test_get_multiples():
    result = get_multiples([3,4,2,1,3,3], {4:1,3:3,5:1,9:1})
    assert([9,4,0,0,9,9]) == result