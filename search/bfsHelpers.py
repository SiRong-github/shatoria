from queue import Queue
from .constants import *
from .v_helpers import *

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
        for neighbour in neighbours(token, board):
            if (neighbour not in visited):
                q.put(neighbour)

    return q


"""Gets adjacent edges (neighbours)"""


def neighbours(token, board):
    neighbours = []
    u = token[0]
    neighboursIndex = [u + up, u + upLeft, u + upRight,
                       u + down, u + downLeft, u + downRight]

    for neighbourIndex in neighboursIndex:
        check_bounds(neighbourIndex)

        for item in board:
            if (item[0] == neighbourIndex):
                neighbours.append(item)

    return neighbours

def get_first_red_cell(board):
    """Finds first red cell in board to start BFS from"""

    for coordinates, attributes in board.items():
        if (attributes[0] == "r"):
            return coordinates