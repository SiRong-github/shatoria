import math
from .constants import *
from .actions_helpers import *
from queue import PriorityQueue

def euclidean_astar_search(board, actions_list):
    """Infects blue cells with A* search, with manhattan distance as a heuristic. Stops when all blue cells are infected"""

    # Right now it doesn't store knowledge of past moves and expands AT ONCE. It doesn't come up with a path first and Then expands, and that's an issue. 

    # + it's oversetimating the path costs because it doesn't take power into account. so if A -> B should only take one move because of power, right now our heuristic is saying it would take three moves. not admissible

    # i think i should reframe how i want to solve this problem

    # if BFS allows us to reach optimal solution we can also just go for bfs

    closest_blues = get_closest_blues(board)
    reds, blues = get_red_blue_cells(board)
    blue_count = len(blues)

    # priority queue of red cells, prioritized on their distance to their closest, `target` blue cell.
    pq = PriorityQueue()
    for key, value in closest_blues.items():
        pq.put((value[1], key + value[0]))

    # number of moves made so far
    num_moves = 0
    
    while blue_count != 0:

        # always target closest blue cell we can get to, expand cells targetting this specific cell until it is infected
        while True:
            red_blue_pair = pq.get()[1]
            to_expand = (red_blue_pair[0], red_blue_pair[1])
            target = (red_blue_pair[2], red_blue_pair[3])

            blue_infected, new_reds = expand_cell(to_expand, target, board, actions_list)

            for red_cell_rq in new_reds:
                closest_blues[red_cell_rq] = (target, get_distance(red_cell_rq, target))
                pq.put((closest_blues[red_cell_rq][1], red_cell_rq + target))

            del closest_blues[to_expand]
            
            if blue_infected:
                # print("Infected!") 
                break
        
        reds, blues = get_red_blue_cells(board)
        blue_count = len(blues)
        closest_blues = get_closest_blues(board)

        pq = PriorityQueue()
        for key, value in closest_blues.items():
            pq.put((value[1], key + value[0]))

    return

def expand_cell(red_cell_rq, target_blue_cell, board, actions_list):
    """Expand cell in best direction to spread to (the one which brings it closer to its target cell"""

    # initialize var to store best direction to spread to
    best_direction = (tuple(), 10)

    for direction in DIRECTIONS:
        new_red_cell_rq = (red_cell_rq[0] + direction[0], red_cell_rq[1] + direction[1])

        # distance from new cell to target blue cell
        new_dist = get_distance(new_red_cell_rq, target_blue_cell)

        if (new_dist < best_direction[1]):
            best_direction = (direction, new_dist)

    # just need to keep direction now
    best_direction = best_direction[0]
    
    return spread(red_cell_rq[0], red_cell_rq[1], best_direction[0], best_direction[1], board, actions_list)

def get_closest_blues(board):
    """Return a dictionary with coordinates of each red cell on the board as keys. Each key has a tuple value of (`closest blue cell to the red cell`, `distance to that red cell`)"""

    closest_blues = dict()

    reds, blues = get_red_blue_cells(board)

    # for each red cell
    for red_cell in reds:
        red_cell_rq = red_cell[0]

        # find blue cell closest to the red cell
        for blue_cell in blues:
            blue_cell_rq = blue_cell[0]
            distance = get_distance(red_cell_rq, blue_cell_rq)

            if (red_cell_rq not in closest_blues):
                closest_blues[red_cell_rq] = (blue_cell_rq, distance)

            elif (distance < closest_blues[red_cell_rq][1]):
                closest_blues[red_cell_rq] = (blue_cell_rq, distance)

    return closest_blues

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

def get_distance(red_cell_rq, blue_cell_rq):
    """Get manhattan distance between a red cell and blue cell"""

    r_dist = min(abs(red_cell_rq[0] - blue_cell_rq[0]), 6 - abs(red_cell_rq[0] - blue_cell_rq[0]))
    q_dist = min(abs(red_cell_rq[1] - blue_cell_rq[1]), 6 - abs(red_cell_rq[1] - blue_cell_rq[1]))

    return q_dist + r_dist