from src.geography import Cordinate
from typing import List
import matplotlib.pyplot as plt


def around_cordinate(x0, y0, max = 0, __start = 0, __end = None):
    for x in range(x0-max, x0+max+1) if not __end else range(__start, __end):
        for y in range(y0-max, y0+max+1) if not __end else range(__start, __end):
            if x == x0 and y == y0:
                continue
            yield (x, y) 


def diagonal_cordinate(x0, y0, max = 0, __start = 0, __end = None):
    def line_func(m, point):
        def wapper(x):
            return m*(x - point[0]) + point[1]
        return wapper
    
    line13 = line_func(1, (x0, y0))
    line24 = line_func(-1, (x0, y0))

    for x in range(max+1) if not __end else range(__start, __end):
        p = (x, line13(x))
        if p[0] == x0 and p[1] == y0:
            continue
        yield p
    for x in range(max+1) if not __end else range(__start, __end):
        p = (x, line24(x))
        if p[0] == x0 and p[1] == y0:
            continue
        yield p


def new_diagonal_cordinate(x0, y0, __start = 1, __end = 8):
    def line_func(m, point):
        def wapper(x):
            return m*(x - point[0]) + point[1]
        return wapper
    
    line13 = line_func(1, (x0, y0))
    line24 = line_func(-1, (x0, y0))

    top_right = [(x, line13(x)) for x in range(x0 + 1, __end + 1)]
    down_left = [(x, line13(x)) for x in range(x0 - 1, __start - 1, -1)]

    top_left = [(x, line24(x)) for x in range(x0 - 1, __start - 1, -1)]
    down_right = [(x, line24(x)) for x in range(x0 + 1, __end + 1)]

    return [
        top_right, top_left, down_left, down_right
    ]


def flat_cordinate(x0, y0, max = 0, __start_x = 0, __end_x = 0, __start_y = 0, __end_y = 0):
    for x in range(max+1) if not (__start_x and __end_x) else range(__start_x, __end_x):
        p = (x, y0)
        if p[0] == x0 and p[1] == y0:
            continue
        yield p
    for y in range(max+1) if not (__start_y and __end_y) else range(__start_y, __end_y):
        p = (x0, y)
        if p[0] == x0 and p[1] == y0:
            continue
        yield p


def new_flat_cordinate(x0, y0, __start_x = 1, __end_x = 8, __start_y = 1, __end_y = 8):

    right = [(x, y0) for x in range(x0 + 1, __end_x + 1)]
    left = [(x, y0) for x in range(x0 - 1, __start_x - 1, -1)]

    top = [(x0, y) for y in range(y0 + 1, __end_y + 1)]
    down = [(x0, y) for y in range(y0 - 1, __start_y - 1, -1)]

    return [
        right, top, left, down
    ]


def l_move_cordinate(x0, y0):
    all = list(around_cordinate(x0, y0, 2))

    for x in diagonal_cordinate(x0, y0, __start = x0 - 2, __end = x0 + 3):
        if x in all:
            all.remove(x)
    for x in flat_cordinate(
        x0, y0, __start_x = x0 - 2, 
        __end_x = x0 + 3, __start_y = y0 - 2, 
        __end_y = y0 + 3):

        if x in all:
            all.remove(x)
    for x in all:
        yield x


def queen_move_cordinate(x0, y0):
    dia =  list(diagonal_cordinate(x0, y0, 8))
    flat = list(flat_cordinate(x0, y0, 8))
    for x in dia + flat:
        yield x


def new_queen_move(x0, y0):
    dia = new_diagonal_cordinate(x0, y0)
    flat = new_flat_cordinate(x0, y0)
    return flat + dia


def show_scatter(cordinates: List[Cordinate]):
    x = []
    y = []
    for p in cordinates:
        x.append(p.column.value)
        y.append(p.row.value)
    plt.scatter(x, y)
    plt.show()

        
