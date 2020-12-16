from enum import Enum
from .erorrs import CantGoBackward, CantMoveForward

class Column(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8

    def forward(self, count):
        to_move = self.value + count
        if to_move > 8:
            raise CantMoveForward(count)
        return Row(to_move)

    def backward(self, count):
        to_move = self.value - count
        if to_move < 1:
            raise CantGoBackward(count)
        return Row(to_move)


class Row(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8

    def forward(self, count):
        to_move = self.value + count
        if to_move > 8:
            raise CantMoveForward(count)
        return Row(to_move)

    def backward(self, count):
        to_move = self.value - count
        if to_move < 1:
            raise CantGoBackward(count)
        return Row(to_move)



class Cordinate:
    def __init__(self, pointer: str = None, column = None, row = None) -> None:
        if pointer:
            nums = Cordinate.pointer_to_num(pointer)
            self.row : Row = Row(nums[1])
            self.column: Column = Column(nums[0])   
        else:
            if not row or not column:
                raise ValueError('Not enough values!')
            self.row : Row = row
            self.column: Column = column

    def __str__(self) -> str:
        columns = {1: 'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}
        return f"{columns[self.column.value]}{self.row.value}"

    def __eq__(self, o: object) -> bool:
        return self.column == o.column and self.row == o.row

    def __repr__(self) -> str:
        return f"({self.column}, {self.row})"

    @staticmethod
    def make_cordinate(x, y):
        return Cordinate(column= Column(x), row= Row(y))

    def is_equal(self, other = None, row = None, column = None) -> bool:
        if row and column:
            return self.column.value == column and self.row.value == row

        if not isinstance(other, Cordinate):
            raise TypeError('Need a cordinate obj')

        return self.column.value == other.column.value and \
             self.row.value == other.row.value
    
    @staticmethod
    def pointer_to_num(pointer: str):
        __pointer_part1 = "abcdefgh"
        __pointer_part2 = "12345678"

        if pointer and isinstance(pointer, str):
            pointer = pointer.lower()
            if pointer.__len__() == 2:
                if pointer[0] in __pointer_part1 and pointer[1] in __pointer_part2:
                    return (
                        __pointer_part1.find(pointer[0]) + 1,
                        __pointer_part2.find(pointer[1]) + 1
                    )   
        raise ValueError('pointer not valid use like: e4')    

    @staticmethod
    def from_pointer(pointer: str):
        nums = Cordinate.pointer_to_num(pointer)
        return Cordinate(column= Column(nums[0]), row= Row(nums[1]))
        




class Team(Enum):
    Black = 0
    White = 1