# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from .heuristic import *
from .astar_mega_relaxed import *
import timeit


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    start = timeit.default_timer()
    solution = astar_search(input)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    return solution