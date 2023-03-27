from queue import PriorityQueue
import math
from .constants import *
from .actions_helpers import *

def euclidean_search(red, blue, board, actions_list):
    """Infects blue cells with A* search, with euclidean distance as a heuristic. Stops when all blue cells are infected"""

    # heuristic = euclidean distance to closest blue cell (math.dist())

    # stop when all blue cells are colonized

    # initialize dict with each red cell as keys, with values in a tuple of format: (`closest blue cell coordinate`, `distance to closest blue cell`)
    closest_blues = dict()
    for red_cell in red:
        red_cell_rq = red_cell[0]

        for blue_cell in blue:
            blue_cell_rq = blue_cell[0]
            distance = math.dist(red_cell_rq, blue_cell_rq)

            if (red_cell not in closest_blues):
                closest_blues[red_cell_rq] = (blue_cell_rq, distance)
            elif (distance < closest_blues[red_cell_rq][1]): # no tiebreaking for now
                closest_blues[red_cell_rq] = distance

    for red_cell_rq in closest_blues.keys():
        expand_cell(red_cell_rq, closest_blues, board, actions_list)
    
    # how to update grid when a blue cell has been colonized?

    # how to update red cells when they've spread?
        # ok for now we just have to update distance of NEW red cells to closest blue cell

    return

def expand_cell(red_cell_rq, closest_blues, board, actions_list):
    # expand cell in best direction to spread to (the one which brings it closer to the cell in closest_blues)

    # initialize var to store best direction to spread to
    best_direction = (tuple(), 10)

    for direction in DIRECTIONS:
        new_red_cell_rq = (red_cell_rq[0] + direction[0], red_cell_rq[1] + direction[1])

        # distance from new cell to target blue cell
        new_dist = math.dist(new_red_cell_rq, closest_blues[red_cell_rq][0])

        if (new_dist < best_direction[1]):
            best_direction = (direction, new_dist)

    # just need to keep direction now
    best_direction = best_direction[0]

    spread(red_cell_rq[0], red_cell_rq[1], best_direction[0], best_direction[1], board, actions_list)
    
    return