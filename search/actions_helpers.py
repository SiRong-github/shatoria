MIN_COORDINATE = 0
MAX_COORDINATE = 6


def spread(r, q, dr, dq, board, actions_list):
    """Spreads a red cell (r, q) to the direction (dr, dq). Updates board and list of actions accordingly. Returns True if any blue cell was infected"""
    blue_infected = False

    parent_cell = (r, q)

    if not valid_spread(parent_cell, board):
        return False

    curr_power = get_power((r, q), board)

    spread_cell = (r + dr, q + dq)
    while (curr_power != 0):
        spread_cell = check_bounds(spread_cell)
        print(f"Spreading to:{spread_cell}")

        if (spread_cell not in board):
            board[spread_cell] = ("r", 1)

        else:
            if (get_color(spread_cell, board) == "b"):
                blue_infected = True
            board[spread_cell] = ("r", get_power(spread_cell, board) + 1)

        curr_power -= 1
        spread_cell = (spread_cell[0] + dr, spread_cell[1] + dq)

    actions_list.append(parent_cell + (dr, dq))

    # Empty parent cell
    del board[(r, q)]

    return blue_infected


def valid_spread(cell, board):
    """Return true if it's possible to spread cell (r, q), and false otherwise."""

    return ((cell in board) or (get_color(cell, board) == "r"))


def check_bounds(cell):
    """If coordinates of a new cell is beyond the bounds of the board when spreading, adjust so that ___. """

    if (cell[0] < MIN_COORDINATE):
        cell = (cell[0] % (MAX_COORDINATE+1), cell[1])
    elif (cell[0] > MAX_COORDINATE):
        cell = (cell[0] % (MAX_COORDINATE+1), cell[1])

    if (cell[1] < MIN_COORDINATE):
        cell = (cell[0], cell[1] % (MAX_COORDINATE+1))
    elif (cell[1] > MAX_COORDINATE):
        cell = (cell[0], cell[1] % (MAX_COORDINATE+1))

    return cell


def get_color(cell, board):
    """Returns color of cell (r, q) in board."""

    return board[cell][0]


def get_power(cell, board):
    """Returns power of cell (r, q) in board."""

    return board[cell][1]
