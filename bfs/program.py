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