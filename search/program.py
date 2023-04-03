# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from queue import Queue
from queue import PriorityQueue
from .bfsSolver import *

import timeit


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a
    # board state in a human-readable format. Try changing the ansi argument
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=True))
    print(input)

    # Solution based on BFS
    # Input: type dictionary input of board state
    # Output: list of actions to conquer all blue tokens

    start = timeit.default_timer()
    solution = bfsSolver(input)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return solution

    # Space-Time Trade-Off
    # It is more efficient to use a dictionary for lookup of elements because it takes less time to traverse in the dictionary than a list.
    # Checking for membership of a value in a set (or dict, for keys) is blazingly fast (taking about a constant, short time), while in a list it takes time proportional to the list's length in the average and worst cases
    # Maybe we don't have to convert dictionary to list???

    # MIGHT BE HELPFUL FOR DISTANCE/SPREAD CHECKING
    # You can look up the current occupancy/power of a cell using a coordinate tuple (r, q) as a key.
    # Just keep in mind that not all cells are necessarily occupied (the dictionary is a sparse representation), so check that the key exists before using it.

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    # return [
    #     (5, 6, -1, 1),
    #     (3, 1, 0, 1),
    #     (3, 2, -1, 1),
    #     (1, 4, 0, -1),
    #     (1, 3, 0, -1)
    # ]
