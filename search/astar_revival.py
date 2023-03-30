from .constants import *
from .actions_2 import *
from .actions_helpers import *
from queue import PriorityQueue

def astar_search(board):
    """Conducts A star search on board. Returns list of actions to get to goal state."""

    # Priority queue of board states
    # Each board state has to retain f(n) = current node depth + g(n)

    # priority queue depth but where do we start
    total_index = 1

    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "score": None,
                "depth": 0,
                "most_recent_move": None,
                "children": None
    }

    root_node["score"] = root_node["depth"] + get_board_score(board)
    print(root_node)

def generate_children(parent_board, queue, total_index):
    """Generate all possible children of a board state. Add to priority queue"""

    red, blue = get_red_blue_cells(parent_board)

    # for each red cell in board state
    for red_cell in red:

        # expand red cell in all the possible directions
        for direction in DIRECTIONS:
            child_state = spread2(red_cell, direction, parent_board)
            create_node(red_cell, child_state, (red_cell + direction),total_index)
        # evaluate 'score' of state
        # add to PQ

def get_board_score(board):
    """Gets sum of distances of blue cell to their closest red cells - intuitively the closer a red cell is to a blue cell the closer we can get to infect them, winning the game"""

    sum_minimum_distances = 0
    reds, blues = get_red_blue_cells(board)

    for blue_cell in blues:
        blue_cell_rq = blue_cell[0]
        min_distance = 10

        for red_cell in reds:
            red_cell_rq = red_cell[0]
            distance = get_distance(red_cell_rq, blue_cell_rq)

            if distance < min_distance:
                min_distance = distance
                min_red_cell = red_cell

        sum_minimum_distances += min_distance

    return sum_minimum_distances

def get_distance(red_cell_rq, blue_cell_rq):
    """Get manhattan distance between a red cell and blue cell"""

    r_dist = min(abs(red_cell_rq[0] - blue_cell_rq[0]), 6 - abs(red_cell_rq[0] - blue_cell_rq[0]) + 1)
    q_dist = min(abs(red_cell_rq[1] - blue_cell_rq[1]), 6 - abs(red_cell_rq[1] - blue_cell_rq[1]) + 1)

    return q_dist + r_dist

def create_node(parent_state, new_state, new_move, total_index):
    """Creates new "node" structure, given a new board state"""

    new_node = {"id": total_index + 1,
                "board": new_state,
                "parent_id": parent_state["id"],
                "score": None,
                "depth": parent_state["depth"] + 1,
                "most_recent_move": new_move,
                "children": None
    }

    new_node["score"] = new_node["depth"] + get_board_score(new_state)

    return new_node

def is_goal_state(board):
    "Returns whether or not an input board is a goal state"

    reds, blues = get_red_blue_cells(board)
    
    return len(blues) == 0