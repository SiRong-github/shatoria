import numpy as np
from queue import Queue
from .constants import *
from .actions_helpers import *
from .actions_helpers import *


# Vertex -> list of vertices // pq??? priority = 0, then data beside it
# Edge -> list of tuples (edges)

marked = []

"""Breadth First Search Algorithm"""


def bfs(start, board):

    # Initialise variables
    visited = []
    q = Queue(limit)
    q.put(start)

    # Loop through vertices
    while q.not_empty:

        token = q.get()
        visited.append(token)

        print("token")
        print(token)
        print(type(token))
        print("\n")

        for neighbour in neighbours(token, board):
            if (neighbour not in visited):
                q.put(neighbour)

    return q


"""Gets adjacent edges (neighbours)"""


def neighbours(token, board):

    neighbours = []
    neighboursIndex = []

    u = token[0]
    power = 14  # token[1][1]

    print("u")
    print(u)
    print("power")
    print(power)
    print("\n")

    for i in range(1, power+1):
        neighboursIndex.append(addTuples(u, multiplyPower(up, i)))
        neighboursIndex.append(addTuples(u, multiplyPower(upLeft, i)))
        neighboursIndex.append(addTuples(u, multiplyPower(upRight, i)))
        neighboursIndex.append(addTuples(u, multiplyPower(down, i)))
        neighboursIndex.append(addTuples(u, multiplyPower(downLeft, i)))
        neighboursIndex.append(addTuples(u, multiplyPower(downRight, i)))

    print("\n")
    for neighbourIndex in neighboursIndex:
        print("neighbourIndex before")
        print(neighbourIndex)
        neighbourIndex = check_bounds(neighbourIndex)
        print("neighbourIndex after")
        print(neighbourIndex)
        print("\n")

        # for item in board:
        #     print(item)
        #     print(type(item))
        #     print(item[0])
        #     print(type(item[0]))
        #     if (item[0] == neighbourIndex):
        #         print("item")
        #         print(item)
        #         neighbours.append(item)

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
