from .actions_helpers import *
from .constants import *
from itertools import combinations

# we actually don't even have to do ids
def heuristic(board):
    """Finds estimate of minimum number of moves to get from board state to goal state by finding optimal solution for relaxed Infexion board where red cells can ONLY jump to blue cells, multiple times in one move according to the power it has. Returns optimal number of moves to get to goal state."""

    # store nodes as value with their index as key
    curr_board = board.copy()

    num_moves = 0
    while not is_goal_board(curr_board):
        curr_board = generate_board_child(curr_board)
        num_moves += 1
 
    return num_moves # delete len later

def generate_board_child(parent_board):
    """Generate most optimal successor of relaxed game's `parent_board`'s state. Returns child board configuration."""

    reds, blues = get_red_blue_cells(parent_board)

    # always spread red with highest power
    sorted_reds = sorted(reds, key=lambda cell: cell[1][1])
    to_spread = sorted_reds[0]

    # always infect blue cells with highest powers first since they'll result in high-power red cells, so we can get to shortest possible moves faster
    sorted_blues = sorted(blues, key=lambda cell: cell[1][1])

    # avoid out of bounds list index in cases where power of red cell > num of blue cells left
    power = get_power(to_spread[0], parent_board)
    if (power) > len(blues):
        power = len(blues)

    spread_targets = [blue_cell[0] for blue_cell in sorted_blues[:power]]

    curr_board = parent_board.copy()
    for blue_cell_rq in spread_targets:
        curr_board = spread_relaxed(to_spread, blue_cell_rq, curr_board)
    child_board = curr_board
    
    # print(render_board(child_board, ansi=True))

    return child_board

def is_goal_board(board):
    "Returns whether or not a board has reached goal state"

    reds, blues = get_red_blue_cells(board)
    
    return len(blues) == 0