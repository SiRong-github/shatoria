"""
Breadth First Search Algorithm
"""

# Imports
import queue
from .constants import *
from .actions_helpers import *
from .tupleOperators import *

# Functions


def getReds(board, reds):
    """
    Stores red tokens of a given board state into a given dictionary
    Input: board dictionary, red tokens dictionary
    Output: None
    """

    for key, value in board.items():
        if value[0] == 'r':
            reds.update({key: value})
    return


def redWins(board):
    """
    Checks if blue tokens have been conquered in a given board state
    Input: board dictionary
    Output: boolean result of whether red wins
    """

    # Return if moves or board is null
    if not board:
        return False

    # Check if red wins
    for value in board.values():
        if value[0] == 'b':
            return False
    return True


def bfsSolver(board):
    """
    Uses BFS strategy for red to win
    Input: board dictionary
    Output: List of tuples demonstrating sequence of SPREAD actions
    """

    reds = {}  # (r, q) : (player, k)
    possibleMoves = queue.Queue()  # queue of list of moves
    moves = []  # [(r, q, dr, dq), ...]
    visitedBoards = {}  # (r, q) : True
    paths = {}  # id: {direction, board, moves}; possible pathways of the game
    newBoard = dict(board)  # create copy of board

    # Get red tokens of board
    getReds(board, reds)

    # Initialise queue with red tokens on initial board
    for key in reds.keys():
        possibleMoves.put((key+(0, 0)))  # (r, q, dr, dq)

    # Search for possible solutions to conquer BLUE
    while not possibleMoves.empty():

        # Expand possible moves of RED
        currMoves = possibleMoves.get()
        if (type(currMoves) == tuple):
            moves = [currMoves]
        else:
            moves = currMoves

        if paths:
            # Search for a similar board state in the paths dictionary to avoid recreating
            for id in range(len(paths)):
                moves2 = paths[id]["moves"]
                board2 = paths[id]["board"]
                visited2 = paths[id]["visited"]
                count = 0
                if len(moves2) == len(moves)-1:
                    for move2 in moves2:
                        if move2 not in moves:
                            break
                        else:
                            count = count + 1
                # Found similar board state
                if count == len(moves2):
                    expandMoves(moves, board2, visited2, paths)
                    break
        else:
            visited = {}
            expandMoves(moves, board, visited, paths)

        # Check if red wins based on newly created paths
        for i in range(len(paths)):
            if i not in visitedBoards:
                visitedBoards[i] = True
                newBoard = paths[i]["board"]
                moves = paths[i]["moves"]
                # Convert type if required
                if type(moves) == tuple:
                    moves = [moves]
                # Return move if won
                if redWins(newBoard):
                    return moves
                # Account for new red tokens in possible moves
                reds = {}
                getReds(newBoard, reds)
                for key in reds.keys():
                    if moves:
                        newMoves = moves.copy()
                        newMoves.append((key+(0, 0)))
                    else:
                        newMoves = [((key+(0, 0)))]
                    possibleMoves.put(newMoves)

    return [(0, 0, 0, 0)]  # no solution


def expandMoves(moves, board, visited, paths):
    """
    Expands possible moves in a given board state
    Input: board dictionary, list of moves containing (r, q, dr, dq)
    Output: None
    """

    # Find possibilities for each move
    for move in moves:

        cell = (move[0], move[1])

        # Skip if invalid (not in board) or already visited
        if cell not in board.keys() or cell in visited.keys():
            continue

        # Get power
        k = board[cell][1]

        # Get possible moves
        for d in DIRECTIONS:

            # make new copies
            newBoard = dict(board)
            newVisited = dict(visited)
            newMoves = moves.copy()

            # Store possible moves
            possibleMove = ()
            possibleMove = possibleMove + (cell + d)
            if newMoves:
                for new in newMoves:
                    if (new[2] == 0 and new[3] == 0):
                        newMoves.remove(new)
                newMoves.append(possibleMove)
            else:
                newMoves = possibleMove

            # Get new cells of each move based on power
            for i in range(1, k+1):
                newCell = check_bounds(addTuples(cell, multiplyPower(d, i)))

                # Update if cell not empty, else spread
                if newCell in newBoard.keys():
                    prevK = newBoard[newCell][1]
                    newBoard[newCell] = ('r', prevK+1)
                else:
                    newBoard[newCell] = ('r', 1)

            # Empty cell and mark visited
            del newBoard[cell]
            newVisited[cell] = True

            # Store in dictionary
            id = len(paths)
            paths[id] = {"direction": d,
                         "board": newBoard,
                         "moves": newMoves,
                         "visited": newVisited}

    return
