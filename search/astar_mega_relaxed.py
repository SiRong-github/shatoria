from .constants import *
from .actions_helpers import *
from .ids import *
from queue import PriorityQueue
from .utils import render_board

def astar_search(board):
    """Conducts A star search on board. Returns list of actions to get to goal state."""

    all_states = dict()
    pq = PriorityQueue()

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
    all_states[1] = root_node

    pq.put((root_node["score"], root_node["id"]))
    current_node = all_states[pq.get()[1]]
    print("score:", current_node["score"])

    i = 0

    while not is_goal_state(current_node):
        for child_node in generate_children(current_node, total_index):
            all_states[child_node["id"]] = child_node
            pq.put((child_node["score"], child_node["id"]))
            # print(render_board(child_node["board"], True))
            total_index += 1
        i += 1

        #while not pq.empty():
         #   print(pq.get())

        #print("DONE")
        # print(render_board(current_node["board"], True))
        current_node = all_states[pq.get()[1]]
        #print(render_board(current_node["board"], True))
        
    moves_made = list()
    while current_node["parent_id"] != None:
        # print(render_board(current_node["board"], True))
        moves_made.insert(0, current_node["most_recent_move"])
        current_node = all_states[current_node["parent_id"]]
        print(current_node["score"])
    
    return moves_made

def generate_children(parent_state, total_index):
    """Generate all possible children of a board state. Add to priority queue"""
    parent_board = parent_state["board"]
    red, blue = get_red_blue_cells(parent_board)

    child_nodes = list()
    # for each red cell in board state
    for red_cell in red:

        # expand red cell in all the possible directions
        for direction in DIRECTIONS:
            # print(parent_board)
            child_board = spread(red_cell, direction, parent_board)
            child_node = create_node(parent_state, child_board, (red_cell[0] + direction), total_index)
            
            child_nodes.append(child_node)
            total_index += 1
            # print(render_board(child_board, ansi=True))
        # evaluate 'score' of state
        # add to PQ

    return child_nodes

def get_board_score(board):
    """Returns number of moves needed to clear game, assuming that red cell can jump to any blue cell for each power unit it has"""

    reds, blues = get_red_blue_cells(board)


    return len(blues)

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

def create_node(parent_state, new_state, new_move, total_index):
    """Creates new "node" structure, given a new board state"""

    new_node = {"id": total_index + 1,
                "board": new_state,
                "parent_id": parent_state["id"],
                "depth": parent_state["depth"] + 1,
                "most_recent_move": new_move,
                "children": None
    }

    return new_node