from .actions_helpers import *

def spread2(cell, direction, board):
    """Spreads a cell in desired direction. Returns resulting board"""

    copied_board = board.copy()

    if not valid_spread(cell, copied_board):
        return False
    
    cell_rq = cell[0]
    curr_power = get_power(cell_rq, copied_board)

    spread_cell = (cell_rq[0] + direction[0], cell_rq[1] + direction[1])
    while (curr_power != 0):
        spread_cell = check_bounds(spread_cell)
        # print(f"Spreading to:{spread_cell}")

        if (spread_cell not in copied_board):
            copied_board[spread_cell] = ("r", 1)

        else:
            copied_board[spread_cell] = ("r", get_power(spread_cell, copied_board) + 1)

        curr_power -= 1

        spread_cell = (spread_cell[0] + direction[0], spread_cell[1] + direction[1])

    # Empty parent cell
    del copied_board[(cell_rq[0], cell_rq[1])]

    return copied_board

def get_red_blue_cells(board):
    """Return list of red and blue cells (including their power and color)"""
    red = list()
    blue = list()

    for item in board.items():
        if (item[1][0] == 'r'):
            red.append(item)
        else:
            blue.append(item)
    
    return red, blue