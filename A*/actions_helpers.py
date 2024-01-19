from .utils import render_board
from .constants import *

def spread(cell, direction, board):
    """Spreads a cell in desired direction. Returns resulting board"""

    copied_board = board.copy()

    cell_rq = cell[0]
    if not valid_spread(cell_rq, copied_board):
        return False
    
    curr_power = get_power(cell_rq, copied_board)

    # Spreads cells across board in `direction` according to `cell`'s power
    spread_cell = (cell_rq[0] + direction[0], cell_rq[1] + direction[1])
    while (curr_power != 0):
        spread_cell = check_bounds(spread_cell)

        # spread to an empty space
        if (spread_cell not in copied_board):
            copied_board[spread_cell] = ("r", 1)

        # delete destination cell from board if its power is above 6
        elif (get_power(spread_cell, copied_board) + 1 > MAX_COORDINATE):
            del copied_board[spread_cell]

        # add to power of existing cell and infect it to red
        else:
            copied_board[spread_cell] = ("r", get_power(spread_cell, copied_board) + 1)

        curr_power -= 1
        # next cell to plant on board
        spread_cell = (spread_cell[0] + direction[0], spread_cell[1] + direction[1])

    # remove parent cell from board
    del copied_board[(cell_rq[0], cell_rq[1])]

    return copied_board

def spread_relaxed(cell, destinations, board):
    """Spreads a cell to destination cells in 'relaxed infexion'. Returns resulting board"""

    copied_board = board.copy()
    cell_rq = cell[0]

    for destination_rq in destinations:

        if not valid_spread(cell_rq, copied_board):
            return False

        # delete destination cell from board if its power is above 6
        if (get_power(destination_rq, copied_board) + 1 > MAX_COORDINATE):
            del copied_board[destination_rq]
        
        # add to power of existing cell and infect it to red
        else:
            copied_board[destination_rq] = ("r", get_power(destination_rq, copied_board) + 1)

    # remove parent cell from board
    del copied_board[(cell_rq[0], cell_rq[1])]

    return copied_board

def valid_spread(cell_rq, board):
    """Return true if it's possible to spread cell (r, q), and false otherwise."""

    return ((cell_rq in board) or (get_color(cell_rq, board) == "r"))


def check_bounds(cell):
    """If coordinates of a new cell is beyond the bounds of the board when spreading, adjust so that it teleports to the correct location on the board."""

    if (cell[0] < MIN_COORDINATE):
        cell = (cell[0] % (MAX_COORDINATE+1), cell[1])
    elif (cell[0] > MAX_COORDINATE):
        cell = (cell[0] % (MAX_COORDINATE+1), cell[1])

    if (cell[1] < MIN_COORDINATE):
        cell = (cell[0], cell[1] % (MAX_COORDINATE+1))
    elif (cell[1] > MAX_COORDINATE):
        cell = (cell[0], cell[1] % (MAX_COORDINATE+1))

    return cell


def get_color(cell_rq, board):
    """Returns color of cell (r, q) in board."""

    return board[cell_rq][0]


def get_power(cell_rq, board):
    """Returns power of cell (r, q) in board."""

    return board[cell_rq][1]

def get_red_blue_cells(board):
    """Return list of red and blue cells on board (including their power and color)"""
    red = list()
    blue = list()

    for item in board.items():
        if (item[1][0] == 'r'):
            red.append(item)
        else:
            blue.append(item)
    
    return red, blue

def is_goal_state(node):
    "Returns whether or not a node has reached goal state"

    reds, blues = get_red_blue_cells(node["board"])
    
    return len(blues) == 0