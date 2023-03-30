import numpy as np
from queue import Queue
from .constants import *
from .actions_helpers import *
from .actions_helpers import *


# Vertex -> list of vertices // pq??? priority = 0, then data beside it
# Edge -> list of tuples (edges)

marked = []

"""Breadth First Search Algorithm"""

"""
Assumptions for BFS (no heuristic): 
    first red token as the start state,
    power = 1 so same path cost,
    no knowledge of distance between tokens i.e. which blue node is the closest,
    red token will spread to one of the blue tokens and use the latter's location as the next state
    """


def bfs(start, blues, reds):

    # Initialise variables
    index = start[0]
    power = 1
    visited = []
    possibleMoves = Queue(-1)  # infinitely-sized queue
    newIndices = Queue(-1)  # infinitely-sized queue

    # Conquer all blue tokens in the board
    while len(blues) != 0:

        print("blues not empty")

        blueToken = next(iter(blues.items()))  # tuple
        blueIndex = blueToken[0]

        print("blue token with index")
        print(blueToken)
        print(blueIndex)

        # Reach the current chosen blue token
        while not foundToken(index, blueIndex, possibleMoves):

            print("token not found")

            move = possibleMoves.get()

            print("move")
            print(move)

            for d in DIRECTIONS:
                possibleMoves.put((d, check_bounds(addTuples(index, d))))

        # Prints possible moves
        while not possibleMoves.empty():
            print("possible moves")
            print(possibleMoves.get())

        # Loop through queue
        # while (not possibleMoves.empty()):

        #     for neighbour in neighbours(token, board):
        #         if (neighbour not in visited):
        #             possibleMoves.put(neighbour)

        del blues[blueToken[0]]  # blue token already conquered
        index = blueIndex

    return possibleMoves

    # Loop through vertices
    # while q.not_empty:

    #     token = q.get()
    #     visited.append(token)

    #     print("token")
    #     print(token)
    #     print(type(token))
    #     print("\n")

    #     for neighbour in neighbours(token, board):
    #         if (neighbour not in visited):
    #             q.put(neighbour)

    # print("q empty")


def foundToken(currIndex, goalIndex, moves):

    index = currIndex
    for move in moves:
        possibleMoves.put(check_bounds(addTuples(index, move)))

    possibleMoves.put((d, check_bounds(addTuples(index, d))))

    if index == goalIndex:
        print("Found: " + moves)
        return True

    return False


def getPossibleMoves(token, possibleMoves):

    u = token[0]
    power = 1  # token[1][1]

    # Get possible moves
    for d in DIRECTIONS:
        moves = []
        for i in range(1, power+1):
            moves.append(check_bounds(addTuples(u, multiplyPower(d, i))))
        possibleMoves.put(moves)

    # Prints possible moves
    while not possibleMoves.empty():
        print(possibleMoves.get())


"""Gets moves to reach blue token"""


def reachBlue(index, blueIndex):
    if index == blueIndex:
        return True
    else:
        False


"""Gets adjacent edges (neighbours)"""


def neighbours(token, board):

    neighbours = []
    neighboursIndex = []

    u = token[0]
    power = token[1][1]

    print("u")
    print(u)
    print("power")
    print(power)
    print("\n")

    # Get blue tokens
    blue = {}
    for key, value in board.items():
        if (value[0] == 'b'):
            blue.update({key: value})
        else:
            red.update({key: value})

    for item in board:
        print(item)
        print(type(item))
        print(item[0])
        print(type(item[0]))
        if (item[0] == neighbourIndex):
            print("item")
            print(item)
            neighbours.append(item)

    return neighbours


""""Add tupples (not concatenate) """


def addTuples(a, b):
    return tuple(np.add(np.array(a), np.array(b)))


def multiplyPower(a, b):
    return (a[0] * b, a[1] * b)


def get_first_red_cell(board):
    """Finds first red cell in board to start BFS from"""

    for coordinates, attributes in board.items():
        if (attributes[0] == "r"):
            return coordinates
