# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
# from queue import Queue

up = (1, -1)
upLeft = (0, -1)
upRight = (1, 0)
down = (-1, 1)
downLeft = (-1, 0)
downRight = (0, 1)


def conversionDictNode(input: dict[tuple, tuple]):
    return


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

    # Make nodes

    # queue = queue(343)

    # Append dictionary items to queue

    # for input in input.items():
    #     queue.put(input)

    # for item in queue:
    #     print(item)

    # print(queue[0])
    print(up)

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]
