import math
from .constants import *
from .actions_helpers import *
from queue import PriorityQueue

def euclidean_search(red, blue, board, actions_list):
    """Infects blue cells with A* search, with euclidean distance as a heuristic. Stops when all blue cells are infected"""

    # heuristic = euclidean distance to closest blue cell (math.dist())

    # stop when all blue cells are colonized

    # dict with each red cell as keys, with values in a tuple of format: (`closest blue cell coordinate`, `distance to closest blue cell`)
    closest_blues = dict()

    reds, blues = get_red_blue_cells(board)
    blue_count = len(blues)
    for red_cell in reds:
        update_closest_blue(red_cell, blues, closest_blues)

    pq = PriorityQueue()

    for key, value in closest_blues.items():
        pq.put((value[1], key + value[0])) # (distance, (red cell coordinates, target blue cell coordinates))
    
    while blue_count != 0:
        
    
    # expand cells until we find a solution
    """while (len(blues) != 0)
    
    for red_cell_rq in closest_blues.keys():
        expand_cell(red_cell_rq, blue, closest_blues, board, actions_list)

    # we'll have to remove blue cell when it's been infected"""

    return

def expand_cell(red_cell_rq, target_blue_cell, board, actions_list):
    """Expand cell in best direction to spread to (the one which brings it closer to its target cell"""

    # initialize var to store best direction to spread to
    best_direction = (tuple(), 10)

    for direction in DIRECTIONS:
        new_red_cell_rq = (red_cell_rq[0] + direction[0], red_cell_rq[1] + direction[1])

        # distance from new cell to target blue cell
        new_dist = math.dist(new_red_cell_rq, target_blue_cell)

        if (new_dist < best_direction[1]):
            best_direction = (direction, new_dist)

    # just need to keep direction now
    best_direction = best_direction[0]
    
    return spread(red_cell_rq[0], red_cell_rq[1], best_direction[0], best_direction[1], board, actions_list)

def update_closest_blue(red_cell, blues, closest_blues):
    # right now this doesn't account for the fact that it can leapfrog all the way to the other side. will have to make own function if continue with this

    red_cell_rq = red_cell[0]
    
    for blue_cell in blues:
        blue_cell_rq = blue_cell[0]
        distance = math.dist(red_cell_rq, blue_cell_rq)

        if (red_cell_rq not in closest_blues):
            closest_blues[red_cell_rq] = (blue_cell_rq, distance)

        elif (distance < closest_blues[red_cell_rq][1]): # no tiebreaking for now
            closest_blues[red_cell_rq] = (blue_cell_rq, distance)

def get_red_blue_cells(board):
    red = list()
    blue = list()

    for item in board.items():
        if (item[1][0] == 'r'):
            red.append(item)
        else:
            blue.append(item)
    
    return red, blue