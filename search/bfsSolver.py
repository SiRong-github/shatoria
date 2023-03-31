"""
Breadth First Search Algorithm

Assumptions for BFS (no heuristic):
    1) same path cost so power = 1
    2) no knowledge of distance between tokens i.e. which blue node is the closest
    3) generate possible moves of red tokens and then spread outwards
"""

# Imports
import queue
from .constants import *
from .actions_helpers import *
from .tupleOperators import *

# Functions


def redWins(board):
    """
    Check if blue tokens have been conquered in a given board state
    Input: board of type dictionary
    Output: boolean result of whether red wins
    """

    for value in board.values():
        if (value[0] == 'b'):
            return False
    return True


def getRedsBlues(board, reds, blues):
    """
    Stores red and blue tokens of a given board state into two dictionaries
    Input: board, reds, and blues of type dictionary
    Output: None
    """

    for key, value in board.items():
        if (value[0] == 'b'):
            blues.update({key: value})
        else:
            reds.update({key: value})

    return


def possibleMoves(board, redToken, moves, visited):  # should prolly include visited
    """
    Gets possible moves of a given red token in a given board state
    Input: board state of type dictionary, red token of type tuple, queue of possible moves, cells visited of type dictionary
    Output: new board state of type dictionary
    """

    # Variables
    cell = redToken[0]
    power = redToken[1][1]
    newBoards = queue.Queue()
    moves = queue.Queue()
    moves.put(redToken)

    print("prev board state")
    print(board)

    print("cell")
    print(cell)

    while not moves.empty():
        print("moves queue not empty")

        token = moves.get()
        print("token")
        print(token)

        # Skip token if already visited
        if token[0] in visited:
            continue

        # Mark token as visited, with value (0, 0) indicating that there wasn't any movement
        visited[token] = (0, 0)

        # Get possible moves
        for d in DIRECTIONS:
            move = []
            # Get new cells of each move based on power
            for i in range(1, power+1):
                newCell = check_bounds(addTuples(cell, multiplyPower(d, i)))

                print("direction")
                print(d)
                print("newCell")
                print(newCell)

                move.append((d, newCell))

            newBoard = dict(board)  # make a copy of board for each change

            # For each new cell in move
            for m in move:
                newCell = m[1]

                print("move")
                print(move)
                print("new cell")
                print(newCell)

                if newCell in board.keys():
                    # Conquer blue token if it exists in cell and add to visited dictionary
                    if newBoard[newCell][0] == 'b':
                        prevPower = newBoard[newCell][1]
                        newBoard[newCell] == ('r', prevPower + 1)
                        del newBoard[cell]
                        visited[newCell] = d

                        print("conquered blue board and deleted current cell")

                    else:  # delete after checking
                        print("red in cell, can't spread")

                else:
                    # Spread to cell if empty and add to visited dictionary
                    newBoard[newCell] = ('r', 1)
                    del newBoard[cell]
                    visited[newCell] = d

                    print("spread to new cell and deleted current cell")

                # Store new moves and board to queue
                moves.put(newCell)
                newBoards.put(newBoard)

                print("new board state")
                print(board)

    return moves


def allPossibleMoves(board):
    """
    Gets all possible moves of a given board state
    Input: board of type dictionary
    Output: priority queue of possible moves with their path cost
    """

    # Initialise variables
    allMoves = queue.Queue()
    steps = queue.PriorityQueue()  # stores moves + number of steps
    moves = queue.Queue
    reds = {}
    blues = {}
    visited = {}  # cell as key, direction to cell as value
    # dictionary updates value, if found before can change the direction that lead to the value; cells can appear in diff rows or cols
    # better than traversing thru a list

    # Get red and blue tokens of the board
    getRedsBlues(board, reds, blues)

    # Conquer blue tokens
    while not redWins(board):
        print("not conquered yet")
        for red in reds.items():
            print("red")
            print(red)
            if red not in visited:
                print("red hasn't been visited")
                allMoves.put(possibleMoves(board, red, moves, visited))

        while not allMoves.empty():

            print("queue not empty")

            index = allMoves.get()

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


def bfsSolver(input):
    """
    Uses BFS to help red win
    Input: initial board state of type dictionary
    Output: list of actions to conquer all blue tokens
    """

    # Initialise variables

    board = dict(input)  # create copy of board
    solution = queue.Queue()

    # Conquer all blue tokens until red wins
    while not redWon(board):
        generatePossibleMoves()

    return
