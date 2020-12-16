from src import pieces
from src.pieces import ChessPiece, Pawn, Rook, Kight, Bishop, Queen, King
from typing import List, Union
from .geography import Row, Column, Cordinate, Team
from .erorrs import CaseCheck


class BattleField:
    max_cordinate = Cordinate('h8')
    min_cordibate = Cordinate('a1')
    __validate = False 
    __first_setup = {}
    __moves_record = {}

    def __init__(self, normal_setup = False) -> None:
        if normal_setup:
            self.setup(normal_setup= True)
        else:
            self.__pieces: List[ChessPiece] = []
            
    def setup(self, pattern:dict = {}, normal_setup = False):
        if normal_setup:
            self.__pieces = [
                # White 
                King(Cordinate('e1'), Team.White, self),
                Queen(Cordinate('d1'), Team.White, self),
                Bishop(Cordinate('c1'), Team.White, self),
                Bishop(Cordinate('f1'), Team.White, self),
                Kight(Cordinate('b1'), Team.White, self),
                Kight(Cordinate('g1'), Team.White, self),
                Rook(Cordinate('a1'), Team.White, self),
                Rook(Cordinate('h1'), Team.White, self),
                Pawn(Cordinate('a2'), Team.White, self),
                Pawn(Cordinate('b2'), Team.White, self),
                Pawn(Cordinate('c2'), Team.White, self),
                Pawn(Cordinate('d2'), Team.White, self),
                Pawn(Cordinate('e2'), Team.White, self),
                Pawn(Cordinate('f2'), Team.White, self),
                Pawn(Cordinate('g2'), Team.White, self),
                Pawn(Cordinate('h2'), Team.White, self),

                # Black
                King(Cordinate('e8'), Team.Black, self),
                Queen(Cordinate('d8'), Team.Black, self),
                Bishop(Cordinate('c8'), Team.Black, self),
                Bishop(Cordinate('f8'), Team.Black, self),
                Kight(Cordinate('b8'), Team.Black, self),
                Kight(Cordinate('g8'), Team.Black, self),
                Rook(Cordinate('a8'), Team.Black, self),
                Rook(Cordinate('h8'), Team.Black, self),
                Pawn(Cordinate('a7'), Team.Black, self),
                Pawn(Cordinate('d7'), Team.Black, self),
                Pawn(Cordinate('c7'), Team.Black, self),
                Pawn(Cordinate('b7'), Team.Black, self),
                Pawn(Cordinate('f7'), Team.Black, self),
                Pawn(Cordinate('e7'), Team.Black, self),
                Pawn(Cordinate('g7'), Team.Black, self),
                Pawn(Cordinate('h7'), Team.Black, self),
            ]
            self.__first_setup = BattleField.to_pattern(self.__pieces)
        elif pattern:
            if not isinstance(pattern, dict):
                raise TypeError('Pattern Should be dict!')

            # v  Example
            # patters = {
            #     'e1': ['P', 0]
            # }
            for k, v in pattern.items():
                __piece = None
                if v[0].lower() in ['p', 'pawn']:
                    __piece = Pawn(
                        Cordinate(k), Team(v[1]), self
                    )
                elif v[0].lower() in ['r', 'rook']:
                    __piece = Rook(
                        Cordinate(k), Team(v[1]), self
                    )
                elif v[0].lower() in ['n', 'knight']:
                    __piece = Kight(
                        Cordinate(k), Team(v[1]), self
                    )
                elif v[0].lower() in ['b', 'bishop']:
                    __piece = Bishop(
                        Cordinate(k), Team(v[1]), self
                    )
                elif v[0].lower() in ['q', 'queen']:
                    __piece = Queen(
                        Cordinate(k), Team(v[1]), self
                    )
                elif v[0].lower() in ['k', 'king']: 
                    __piece = King(
                        Cordinate(k), Team(v[1]), self
                    )
                if __piece is None:
                    print(f'Piece for {k} not found')
                else:
                    self.__pieces.append(__piece)
            self.__first_setup = pattern
        else:
            raise ValueError('No pattern no normal setup... what should i do???')
    
    def restore(self):
        self.__pieces = []
        self.setup(self.first_setup)

    @property
    def first_setup(self):
        return self.__first_setup

    @property
    def current_view(self):
        return BattleField.to_pattern(self.__pieces)

    @staticmethod
    def pretty_show(pattern):
        import json
        print(json.dumps(pattern, indent= 4))

    @staticmethod
    def to_pattern(pieces: List[ChessPiece]):
        if isinstance(pieces, list):
            pattern = {}
            for x in pieces:
                if isinstance(x, ChessPiece):
                    if str(x.cordinate) in pattern:
                        raise ValueError('Two piece in a place not allowed!')
                    else:
                        pattern[str(x.cordinate)] = [x.fullname, x.team.value]
                else:
                    raise TypeError('A list of ChessPiece is required!')
            return pattern
        else:
            raise TypeError('A list of ChessPiece is required!')

    def on_move_complete(self, piece, current, last):
        try:
            if self.is_check(piece.team):
                raise CaseCheck()
            print(f'{piece} moved from {last} to {current}')
            return True
        except Exception as e:
            self.move_failed(piece, current, last, str(e))
            return False

    @property
    def is_valid(self):
        return self.__validate

    def check_battlefield(self) -> None:
        found = 0
        for row in range(1, 9):
            for column in range(1, 9):
                for piece in self.__pieces:
                    if piece.cordinate.is_equal(row= row, column= column):
                        found += 1
                if found > 1:
                    raise ValueError(f'More than one piece in a place ({column}{row})')
                found = 0
        self.__validate = True

    def __getitem__(self, value: str):
        return self.find_piece(value)

    def find_piece(self, pointer: str= None, cordinate: Cordinate = None) -> ChessPiece:
        if not cordinate and pointer:
            cordinate = Cordinate.from_pointer(pointer)

        if cordinate is None:
            raise ValueError('Cordinate is none')

        for x in self.__pieces:
            if x.cordinate.is_equal(cordinate):
                return x 

    def has_piece(self, pointer: str= None, cordinate: Cordinate = None) -> bool:
        if not cordinate and pointer:
            cordinate = Cordinate.from_pointer(pointer)

        if cordinate is None:
            raise ValueError('Cordinate is none')

        for x in self.pieces:
            if x.cordinate.is_equal(cordinate):
                return True
        return False

    def move_piece(self, new_location: Union[str, Cordinate], pointer: str= None, cordinate: Cordinate = None):
        p = self.find_piece(pointer, cordinate)
        if p:
            return p.move(new_location)
        raise ValueError('No piece here to move')

    def __setitem__(self, item, value):
        return self.move_piece(value, item)

    def __set_possible_moves(self):
        for piece in self.__pieces:
            piece.find_possible_moves()

    def find_by_tag(self, team, tag):
        for x in self.__pieces:
            if x.team == team:
                if x.tag.lower() == tag.lower():
                    return x

    def is_check(self, team: Team):
        self.__set_possible_moves()
        other_team = Team(0) if team == Team.White else Team(1)
        king = self.find_by_tag(team, 'K')
        for x in [x for x in self.__pieces if x.team == other_team]:
            for m in x.possible_moves:
                if m == king.cordinate:
                    return True
        return False 

    def move_failed(self, piece, current, to_move, msg):
        print(f'{piece} failed to move from {current} to {to_move}, Cuz: {msg}')





        
            

