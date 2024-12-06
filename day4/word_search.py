from __future__ import annotations
from typing import List

def parse_board(data:str) -> List[List[str]]:
    board = []
    rows = data.splitlines()
    for row in rows:
        elements = []
        for charcter in row:
            elements.append(charcter)
        board.append(elements)
    return board


class BoardError(Exception):
    pass

class RowTooBigError(BoardError):
    pass

class ColumnTooBigError(BoardError):
    pass

class Board:
    class BoardIterator:
        def __init__(self, board:Board) -> None:
            self._board = board
            self._col:int = 0
            self._row:int = 0

        @property
        def row(self) -> int:
            return self._row
        
        @row.setter
        def row(self, value:int) -> None:
            if value >= self._board.rows:
                raise RowTooBigError()
            self._row = value
        
        @property
        def col(self) -> int:
            return self._col
        
        @col.setter
        def col(self, value:int) -> None:
            if value >= self._board.columns:
                raise ColumnTooBigError()
            self._col = value
        
        def __iter__(self) -> Board.BoardIterator:
            return self

        def __next__(self) -> str:
            result = self._board[self.row][self.col]

            try:
                self.col += 1
            except ColumnTooBigError:
                try:
                    self.row += 1
                    self.col = 0
                except RowTooBigError:
                    raise StopIteration()

            return result
            
    def __init__(self, data:List[List[str]]):
        self._board:List[List[str]] = data
        self._column = len(data[0])
        self._row = len(data)

    @property
    def rows(self) -> int:
        return self._row
    
    @property
    def columns(self) -> int:
        return self._column
    
    def get_value(self, row:int, column:int) -> str:
        return self._board[row][column]
    
    def __getitem__(self, row:int) -> List[int]:
        return self._board[row]
    
    def __iter__(self):
        return Board.BoardIterator(self)        
            
def search_board(word:str = "XMAS"):
    pass
    

    