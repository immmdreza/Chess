from src.pieces import King, Bishop, Pawn, Queen, Rook, Kight
from src import Row, Column, Cordinate, Team
from src.battlefield import BattleField


if __name__ == "__main__":

    board = BattleField()
    board.setup(
        {
            'e1': ['King', 0],
            'e2': ['Rook', 0],
            'e7': ['Rook', 1]
        }
    )

    if not board.is_valid:
        board.check_battlefield()
        print('Validated')

    # q = board['d1']
    # q.move('D3')

    # same as upper 
    # board.move_piece('D3', 'D1')

    # same as both uppers
    board['e7'] = 'd7'
    board['e1'] = 'd1'

    print(board.is_check(Team.Black))



