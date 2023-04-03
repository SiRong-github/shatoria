from .actions_helpers import *
from .constants import *
from itertools import permutations

def relaxed_ids(board):
    """Conducts ids-like search on relaxed Infexion board where red cells can ONLY jump to blue cells, multiple times in one move according to the power it has. Returns minimum number of moves to get to goal state."""

    total_index = 1

    root_node = {"id": 1,
                "board": board,
                "parent_id": None,
                "depth": 0,
                "children": None,
    }

    # store nodes as value with their index as key
    nodes_dict = dict()
    nodes_dict[1] = root_node

    depth = 0
    solution_node = None
    while True:
        # perform dls up to depth `depth`
        dls_result, total_index = dls(root_node, depth, nodes_dict, total_index)
        # print(total_index)

        if dls_result != None:
            solution_node = dls_result
            break

        depth += 1
        #print("depth:", depth)

    """
    current_node = solution_node
    while current_node["parent_id"] != None:
        print(render_board(current_node["board"], True))
        current_node = nodes_dict[current_node["parent_id"]]"""
 
    return solution_node["depth"], len(nodes_dict) # delete len later

def dls(root_node, depth, nodes_dict, total_index):
    """Performs depth limited search from a root node. Returns None if we have reached max depth but have not found a goal state. Returns solution node otherwise."""

    # always start fresh
    stack = list()
    stack.insert(0, root_node)

    while len(stack) != 0:
        current_node = stack.pop(0)
        #print(render_board(current_node["board"], ansi=True))
        
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
    """Generate all possible children of relaxed game's board state. Returns stack of child nodes"""

    parent_board = parent_state["board"]
    reds, blues = get_red_blue_cells(parent_board)
    blue_rqs = [blue_cell[0] for blue_cell in blues]

    child_nodes = list()
    # for each red cell in board state
    for red_cell in reds:

        # expand red cell until power is exhausted in all possible blue cell orders

        # avoid permutation where n > r
        power = get_power(red_cell[0], parent_board)
        if (power) > len(blues):
            power = len(blues)

        for spread_order in list(permutations(blue_rqs, power)):
            curr_board = parent_board.copy()
            
            for blue_cell_rq in spread_order:
                curr_board = spread_relaxed(red_cell, blue_cell_rq, curr_board)
            child_board = curr_board
            child_node = create_node(parent_state, child_board, total_index)
            child_nodes.insert(0, child_node)
            total_index += 1
            # print(render_board(child_board, ansi=True))

    return child_nodes

def create_node(parent_state, new_state, total_index):
    """Creates new "node" structure, given a new board state"""

    new_node = {"id": total_index + 1,
                "board": new_state,
                "parent_id": parent_state["id"],
                "depth": parent_state["depth"] + 1,
                "children": None
    }

    return new_node