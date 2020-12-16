from abc import ABC
from typing import Callable, List

from .geography import Cordinate, Team
from .erorrs import MoveRestricted
from .helpers import (
    around_cordinate, 
    new_diagonal_cordinate,
    new_flat_cordinate,
    l_move_cordinate, new_queen_move,
)


class ChessPiece(ABC):
    __current_move_count = 0
    __current_cordinate: Cordinate = None
    tag = ''
    fullname = __name__
    __current_possible_moves: List[Cordinate] = []
    __last_position = None

    def __init__(
        self, 
        starting_cordinate: Cordinate, 
        team: Team,
        board,
    ) -> None:
        self.__current_cordinate = starting_cordinate
        self.__last_position = starting_cordinate
        self.__team = team
        self.brd = board

    def __repr__(self) -> str:
        return f"Piece {self.fullname}({str(self.cordinate)})"

    def find_possible_moves(self, board_check: Callable) -> List[Cordinate]:
        pass

    def move(self, pointer: str = None, cordinate: Cordinate = None):
        to_move = None
        if pointer:
            to_move = Cordinate(pointer)
        else:
            if cordinate and isinstance(cordinate, cordinate):
                to_move = cordinate
            else:
                raise ValueError('Use pointer or Cordinate class')
        
        self.find_possible_moves()
        if any([x for x in self.possible_moves if x == to_move]):
            self.__last_position = self.__current_cordinate
            self.__current_cordinate = to_move
            self.__current_move_count += 1
            if not self.brd.on_move_complete(self, self.cordinate, self.__last_position):
                self.__current_cordinate = self.__last_position
                return False
            return True
        raise ValueError('Impossible move!')

    def _set_possible_moves(self, cordinates: List[Cordinate]):
        self.__current_possible_moves = cordinates

    @property
    def possible_moves(self):
        return self.__current_possible_moves

    @property
    def team(self):
        return self.__team

    @property
    def moves_count(self):
        return self.__current_move_count

    @property
    def cordinate(self):
        return self.__current_cordinate

    # @property
    # def moves_preview(self):
    #     show_scatter(self.possible_moves)



class Pawn(ChessPiece):
    tag = 'P'
    fullname = 'Pawn'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        try:
            if self.moves_count == 0:
                cors = [
                    Cordinate(column= self.cordinate.column, row= self.cordinate.row.forward(1)),
                    Cordinate(column= self.cordinate.column, row= self.cordinate.row.forward(2)),
                ]
            else:
                cors = [
                    Cordinate(column= self.cordinate.column, row= self.cordinate.row.forward(1)),
                ]
        except MoveRestricted:
            pass
        for x in cors:
            if self.brd.find_piece(cordinate = x):
                cors.remove(x)
        self._set_possible_moves(cors)
        return cors


class King(ChessPiece):
    tag = 'K'
    fullname = 'King'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        for x in around_cordinate(self.cordinate.column.value, self.cordinate.row.value, 1):
            try:
                cors.append(
                    Cordinate.make_cordinate(x[0], x[1])
                )
            except ValueError:
                pass
        for x in cors:
            p = self.brd.find_piece(cordinate = x)
            if p is not None:
                if p.team == self.team:
                    cors.remove(x)
        self._set_possible_moves(cors)
        return cors


class Bishop(ChessPiece):
    tag = 'B'
    fullname = 'Bishop'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        for dir in new_diagonal_cordinate(self.cordinate.column.value, self.cordinate.row.value):
            for x in dir: 
                try:
                    c = Cordinate.make_cordinate(x[0], x[1])
                    p = self.brd.find_piece(cordinate = c)
                    if p is not None:
                        if p.team != self.team:
                            cors.append(
                                c
                            )                            
                        break
                    cors.append(
                        c
                    )
                except ValueError:
                    pass
        self._set_possible_moves(cors)
        return cors 


class Rook(ChessPiece):
    tag = 'R'
    fullname = 'Rook'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        for dir in new_flat_cordinate(self.cordinate.column.value, self.cordinate.row.value):
            for x in dir:
                try:
                    c = Cordinate.make_cordinate(x[0], x[1])
                    p = self.brd.find_piece(cordinate = c)
                    if p is not None:
                        if p.team != self.team:
                            cors.append(
                                c
                            )                            
                        break
                    cors.append(
                        c
                    )
                except ValueError:
                    pass
        self._set_possible_moves(cors)
        return cors  


class Kight(ChessPiece):
    tag = 'N'
    fullname = 'Kight'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        for x in l_move_cordinate(self.cordinate.column.value, self.cordinate.row.value):
            try:
                cors.append(
                    Cordinate.make_cordinate(x[0], x[1])
                )
            except ValueError:
                pass
        for x in cors:
            p = self.brd.find_piece(cordinate = x)
            if p is not None:
                if p.team == self.team:
                    cors.remove(x)
        self._set_possible_moves(cors)
        return cors     


class Queen(ChessPiece):
    tag = 'Q'
    fullname = 'Queen'

    def __init__(self, starting_cordinate: Cordinate, team: Team, board) -> None:
        super().__init__(starting_cordinate, team, board)

    def find_possible_moves(self) -> List[Cordinate]:
        cors = []
        for dir in new_queen_move(self.cordinate.column.value, self.cordinate.row.value):
            for x in dir:
                try:
                    c = Cordinate.make_cordinate(x[0], x[1])
                    p = self.brd.find_piece(cordinate = c)
                    if p is not None:
                        if p.team != self.team:
                            cors.append(
                                c
                            )                            
                        break
                    cors.append(
                        c
                    )
                except ValueError:
                    pass
        self._set_possible_moves(cors)
        return cors 

    


