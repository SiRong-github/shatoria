# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from queue import Queue
from queue import PriorityQueue
from .bfsHelpers import *


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

    # Initialise variables
    board = []
    red = []
    solutions = PriorityQueue(maxsize=0)
    solution = Queue(maxsize=0)

    # Convert dictionary to list
    for item in input.items():
        board.append(item)
        if (item[1][0] == 'r'):
            red.append(item)

    # MIGHT BE HELPFUL FOR DISTANCE/SPREAD CHECKING
    # You can look up the current occupancy/power of a cell using a coordinate tuple (r, q) as a key.
    # Just keep in mind that not all cells are necessarily occupied (the dictionary is a sparse representation), so check that the key exists before using it.

    for token in red:
        solution = bfs(token, board)
        solutions.append(solution.qsize, solution)

    return solutions.get()

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    # return [
    #     (5, 6, -1, 1),
    #     (3, 1, 0, 1),
    #     (3, 2, -1, 1),
    #     (1, 4, 0, -1),
    #     (1, 3, 0, -1)
    # ]
