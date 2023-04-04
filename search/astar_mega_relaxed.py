from .constants import *
from .actions_helpers import *
from .heuristic import *
from queue import PriorityQueue
from .utils import render_board

def astar_search(board):
    """Conducts A star search on board. Returns list of actions to get to goal state."""

    # Store all nodes that have been explored
    all_states = dict()

    # To store nodes to be expanded, in ascending order of f(n)
    pq = PriorityQueue()

    # Initialize root node
    total_index = 1
    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "score": None,
                "depth": 0,
                "most_recent_move": None,
                "children": None
    }

    nodes_expanded = 1

    root_node["score"] = root_node["depth"] + get_board_score(board, nodes_expanded)[0]
    all_states[1] = root_node

    pq.put((root_node["score"], root_node["id"]))
    current_node = all_states[pq.get()[1]]

    # Run A* search
    while True:
        # Continue generating children until a goal state is reached
        while not is_goal_state(current_node):
            child_nodes, nodes_expanded = generate_children(current_node, total_index, nodes_expanded)
            for child_node in child_nodes:
                all_states[child_node["id"]] = child_node
                pq.put((child_node["score"], child_node["id"]))
                
                total_index += 1

            current_node = all_states[pq.get()[1]]
        
        # Check if any other nodes could still possibly result in an optimal soltuion
        potential_solution = pq.get()
        if potential_solution[0] >= current_node["score"]:
            break
        else:
            current_node = potential_solution[1]
        
    # Reconstruct moves made to get to optimal solution
    moves_made = list()
    while current_node["parent_id"] != None:
        moves_made.insert(0, current_node["most_recent_move"])
        current_node = all_states[current_node["parent_id"]]
    
    nodes_expanded += len(all_states)

    return moves_made

def generate_children(parent_state, total_index, nodes_expanded):
    """Generate all possible children of a parent board state. Returns child nodes"""

    parent_board = parent_state["board"]
    red, blue = get_red_blue_cells(parent_board)

    child_nodes = list()
    # for each red cell in board state
    for red_cell in red:
        # expand red cell in all the possible directions
        for direction in DIRECTIONS:
            child_board = spread(red_cell, direction, parent_board)

            # In the case that the child board has no more red cells but still has blue cells (possible in spread_test.csv for instance), abort expanding the node
            child_red, child_blue = get_red_blue_cells(child_board)
            if len(child_red) == 0 and len(child_blue) != 0:
                continue

            child_node, nodes_expanded = create_node(parent_state, child_board, (red_cell[0] + direction), total_index, nodes_expanded)
            
            child_nodes.append(child_node)
            total_index += 1
    return child_nodes, nodes_expanded

def get_board_score(board, nodes_expanded):
    """Returns number of moves needed to clear game, assuming that red cell can ONLY jump to a blue cell, multiple times in one move according to the power it has. See report.pdf for clearer description"""

    result = heuristic(board)
    nodes_expanded += result

    return result, nodes_expanded

def create_node(parent_state, new_board, new_move, total_index, nodes_expanded):
    """Creates new "node" structure, given a new board"""

    new_node = {"id": total_index + 1,
                "board": new_board,
                "parent_id": parent_state["id"],
                "score": None,
                "depth": parent_state["depth"] + 1,
                "most_recent_move": new_move,
                "children": None
    }

    results = get_board_score(new_board, nodes_expanded)

    new_node["score"] = new_node["depth"] + results[0]

    return new_node, results[1]