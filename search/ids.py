from .actions_2 import *
from .constants import *

def ids(board):
    """Conducts iterative deepening search on board. Returns list of actions to get to goal state."""

    total_index = 1

    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "depth": 0,
                "most_recent_move": None,
                "children": None,
    }

    # store nodes as value with their index as key
    nodes_dict = dict()
    nodes_dict[1] = root_node

    depth = 0
    solution_node = None
    while depth != 7:
        # perform dls up to depth `depth`
        dls_result, total_index = dls(root_node, depth, nodes_dict, total_index)
        # print(total_index)

        if dls_result != None:
            solution_node = dls_result
            break

        depth += 1
        #print("depth:", depth)
        
    moves_made = list()

    # 'traverses up' tree from solution node to reconstruct moves done
    current_node = solution_node
    while current_node["parent_id"] != None:
        # print(render_board(current_node["board"], True))
        moves_made.insert(0, current_node["most_recent_move"])
        current_node = nodes_dict[current_node["parent_id"]]
    
    return moves_made

def dls(root_node, depth, nodes_dict, total_index):
    """Performs depth limited search from a root node. Returns None if we have reached max depth but have not found a goal state. Returns solution node otherwise."""

    # always start fresh
    stack = list()
    stack.insert(0, root_node)

    while len(stack) != 0:
        current_node = stack.pop(0)
        
        #print(current_node["id"])

        # expand node
        if current_node["depth"] != depth:
            if current_node["children"] != None:
                for id in current_node["children"]:
                    stack.insert(0, nodes_dict[id])

            else:
                # expand nodes for 'new' level
                #print("else")
                current_node["children"] = list()

                for child_node in generate_children(current_node, total_index):
                    nodes_dict[child_node["id"]] = child_node
                    stack.insert(0, child_node)

                    current_node["children"].append(child_node["id"])
                    total_index += 1

                #rint([item["id"] for item in stack])
                    
                #print(child_node["id"])

        if is_goal_state(current_node):
            return current_node, total_index
    
    return None, total_index

def generate_children(parent_state, total_index):
    """Generate all possible children of a board state. Returns stack of child nodes"""

    parent_board = parent_state["board"]
    red, blue = get_red_blue_cells(parent_board)

    child_nodes = list()
    # for each red cell in board state
    for red_cell in red:

        # expand red cell in all the possible directions
        for direction in DIRECTIONS:
            # print(parent_board)
            child_board = spread2(red_cell, direction, parent_board)
            child_node = create_node(parent_state, child_board, (red_cell[0] + direction), total_index)
            
            child_nodes.insert(0, child_node)
            total_index += 1
            # print(render_board(child_board, ansi=True))

    return child_nodes

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

def is_goal_state(node):
    "Returns whether or not a node has reached goal state"

    reds, blues = get_red_blue_cells(node["board"])
    
    return len(blues) == 0