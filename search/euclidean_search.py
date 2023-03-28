import math
from .constants import *
from .actions_helpers import *
from queue import PriorityQueue

def euclidean_search(board, actions_list):
    """Infects blue cells with A* search, with distance as a heuristic. Stops when all blue cells are infected"""

    # heuristic = distance to closest blue cell

    # stop when all blue cells are colonized

    # dict with each red cell as keys, with values in a tuple of format: (`closest blue cell coordinate`, `distance to closest blue cell`)

    closest_blues = dict()
    reds, blues = get_red_blue_cells(board)
    blue_count = len(blues)
    for red_cell in reds:
        update_closest_blue(red_cell[0], blues, closest_blues)

    pq = PriorityQueue()

    for key, value in closest_blues.items():
        pq.put((value[1], key + value[0])) # (distance, (red cell coordinates, target blue cell coordinates))
    
    i = 0
    while blue_count != 0 and i < 8:
        j = 0
        while True and j < 5:
            red_blue_pair = pq.get()[1]
            to_expand = (red_blue_pair[0], red_blue_pair[1])
            target = (red_blue_pair[2], red_blue_pair[3])

            blue_infected, new_reds = expand_cell(to_expand, target, board, actions_list)

            for red_cell_rq in new_reds:
                closest_blues[red_cell_rq] = (target, get_distance(red_cell_rq, target))
                pq.put((closest_blues[red_cell_rq][1], red_cell_rq + target))

            del closest_blues[to_expand]

            j += 1
            
            if blue_infected:
                print("Infected!")
                break
        
        reds, blues = get_red_blue_cells(board)
        blue_count = len(blues)

        closest_blues = dict()
        for red_cell in reds:
            update_closest_blue(red_cell[0], blues, closest_blues)

        pq = PriorityQueue()
        for key, value in closest_blues.items():
            pq.put((value[1], key + value[0])) # (distance, (red cell coordinates, target blue cell coordinates))

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

def update_closest_blue(red_cell_rq, blues, closest_blues):
    # right now this doesn't account for the fact that it can leapfrog all the way to the other side. will have to make own function if continue with this
    
    for blue_cell in blues:
        blue_cell_rq = blue_cell[0]
        distance = get_distance(red_cell_rq, blue_cell_rq) #HERE

        if (red_cell_rq not in closest_blues):
            closest_blues[red_cell_rq] = (blue_cell_rq, distance)

        elif (distance < closest_blues[red_cell_rq][1]): # no tiebreaking for now
            closest_blues[red_cell_rq] = (blue_cell_rq, distance)

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

def get_distance(cell1_rq, cell2_rq):
    """Get distance between 2 cells"""

    r_dist = min(abs(cell1_rq[0] - cell2_rq[0]), 6 - abs(cell1_rq[0] - cell2_rq[0]))
    q_dist = min(abs(cell1_rq[1] - cell2_rq[1]), 6 - abs(cell1_rq[1] - cell2_rq[1]))

    return q_dist + r_dist