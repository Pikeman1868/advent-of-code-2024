import pytest
import word_search

@pytest.fixture
def input() -> str:
    return """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def test_parse_board(input):
    expected = [['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'], ['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'], ['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'], ['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'], ['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'], ['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'], ['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'], ['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'], ['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'], ['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']]
    assert expected == word_search.parse_board(input)

class TestBoard():

    @pytest.fixture
    def parsed_board(self, input):
        return word_search.parse_board(input)
    
    @pytest.fixture
    def board(self, parsed_board) -> word_search.Board:
        return word_search.Board(parsed_board)

    def test_board_sets_max_row(self, board:word_search.Board):
        assert 10 == board.rows

    def test_board_sets_max_col(self, board:word_search.Board):
        assert 10 == board.columns

    def test_board_can_iterate_through_elements(self, board:word_search.Board):
        index = 0
        for _ in iter(board):
            index += 1
        assert index == 100
