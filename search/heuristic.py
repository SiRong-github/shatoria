from .actions_helpers import *
from .constants import *
from .utils import render_board

def heuristic(board):
    """Finds estimate of minimum number of moves to get from board state to goal state by finding optimal solution for relaxed Infexion board where red cells can ONLY jump to blue cells, multiple times in one move according to the power it has. Returns optimal number of moves to get to goal state."""

    curr_board = board.copy()
    print("start\n", render_board(curr_board, ansi=True))

    # Play relaxed infexion with optimal moves until goal is reached.
    num_moves = 0
    while not is_goal_board(curr_board):
        curr_board = generate_board_child(curr_board)
        print(render_board(curr_board, ansi=True))
        num_moves += 1
    print("END")
    return num_moves

def generate_board_child(parent_board):
    """Generate most optimal successor of relaxed game's `parent_board`'s state. Returns child board configuration."""

    reds, blues = get_red_blue_cells(parent_board)

    # always spread red with highest power
    sorted_reds = sorted(reds, key=lambda cell: cell[1][1])
    print(sorted_reds)
    to_spread = sorted_reds[0]

    # always infect blue cells with highest powers first (other than 6, since spreading to a power of 6 cell will just remove it) since they'll result in high-power red cells, so we can get to shortest possible moves faster
    sorted_blues = sorted(blues, key=lambda cell: cell[1][1], reverse=True)
    
    sixes_idx = 0
    for blue_cell in sorted_blues:
        if get_power(blue_cell[0], parent_board) != MAX_COORDINATE:
            break
        sixes_idx += 1

    if sixes_idx != 0:
        power_sixes = sorted_blues[:sixes_idx]
        del sorted_blues[:sixes_idx]
        sorted_blues = sorted_blues + power_sixes
    print(sorted_blues)

    # avoid trying to infect more than existing number of blue cells (power of red cell > num of blue cells left)
    power = get_power(to_spread[0], parent_board)
    if (power) > len(blues):
        power = len(blues)

    spread_targets = list()
    for blue_cell in sorted_blues:
        spread_targets.append(blue_cell[0])
        power -= 1

        if power == 0:
            break

    child_board = spread_relaxed(to_spread, spread_targets, parent_board)

    return child_board

def is_goal_board(board):
    "Returns whether or not a board has reached goal state"

    reds, blues = get_red_blue_cells(board)
    
    return len(blues) == 0