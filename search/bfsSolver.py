"""
Breadth First Search Algorithm

Assumptions for BFS (no heuristic): 
    1) same path cost so power = 1
    2) no knowledge of distance between tokens i.e. which blue node is the closest
    3) generate possible moves of red tokens and then spread outwards
"""

# Imports
import numpy as np
from queue import Queue
from .constants import *
from .actions_helpers import *
from .actions_helpers import *

# Functions


def redWon(board):
    """ 
    Check if blue tokens have been conquered
    Input: board of type dictionary
    Output: boolean if red wins 
    """
    for value in board.values():
        if (value[0] == 'b'):
            return False
    return True


def generatePossibleMoves(board):
    """ 
    Takes a board state and generates all possible moves for red tokens on board
    Input: board of type dictionary
    Output: queue of possible moves 
    """

    return


def solver(input):
    """

    """

    # Initialise variables
    reds = {}
    blues = {}
    solutions = PriorityQueue(maxsize=0)
    solution = Queue(maxsize=0)

    # Get blue and red tokens and put them into two dictionaries (this is for the heuristic part i think)
    for key, value in input.items():
        if (value[0] == 'b'):
            blues.update({key: value})
        else:
            reds.update({key: value})

    while (not redWon(input)):
        generatePossibleMoves()

    board = dict(input)  # create copy of board

    while (not redWon(board)):
        generatePossibleMoves()

    return


def bfsSolver(reds, blues):

    # Get first red token in the form of tuple
    firstRed = next(iter(reds.items()))

    # Initialise variables
    index = start[0]
    q = Queue(-1)  # infinitely-sized queue
    q.put(index)

    # for each index in:
    #     d = visited[index]
    # O()
    # O()

    print("index")
    print(index)

    # initialise visited with start cell, use dictionary to search up whether cell is visited
    visited = {index: (0, 0)}  # cell as key, direction to cell as value
    # dictionary updates value, if found before can change the direction that lead to the value; cells can appear in diff rows or cols

    # Conquer all blue tokens in the board
    while len(blues) != 0:

        print("blues not empty")

        blueToken = next(iter(blues.items()))  # tuple
        blueIndex = blueToken[0]

        print("blue token with index")
        print(blueToken)
        print(blueIndex)

        # Search for current blue token
        while not q.empty():

            print("queue not empty")

            index = q.get()

            print("index")
            print(index)

            if index == blueIndex:

                print("token found")

                break
            exploreNeighbours(index, q, visited)

        del blues[blueToken[0]]  # blue token already conquered

        print("\n")

        print("visited")
        for key, value in visited.items():
            print("key")
            print(key)
            print("value")
            print(value)

    return

# Explore neighbours of cell


def exploreNeighbours(index, q, visited):
    for d in DIRECTIONS:
        newIndex = check_bounds(addTuples(index, d))
        print("newIndex")
        print(newIndex)
        q.put(newIndex)
        visited[newIndex] = d
    return

# Add tuples


def addTuples(a, b):
    return tuple(np.add(np.array(a), np.array(b)))
