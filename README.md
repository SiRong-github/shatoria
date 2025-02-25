# University Subject
This is a COMP30024 Artificial Intelligence Project of the University of Melbourne created by a two-person team.

# File Purpose
The program implements a list of SPREAD actions with the lowest cost win sequence for one of the players in a strategic, perfect-information single-player version of the two-player game of contagion and domination called Infexion. Further details are in the File-Level Documentation. For the full version of the game, head to [shatoriaP2](https://github.com/SiRong-github/shatoriaP2). You may also play the game with a friend [here](https://comp30024.pages.gitlab.unimelb.edu.au/2023s1/infexion-playground/).

# File-Level Documentation
Infexion consists of a 7x7 hexagonally-tiled, infinitely repeating board, described by an axial coordinate system in the program. A valid coordinate is an integer pair (r,q), 0 ≤ r ≤ 6, 0 ≤ q ≤ 6. The objective of the players (named Red and Blue) are to conquer all the 'tokens' on the board.

The game ends under three conditions:
    1. One player has successfully controlled all tokens on the board and is thus declared the winner. This can only be done through the SPREAD action. 
    2. If no one has won in 343 turns, the player with the greatest total POWER is the winner, given they lead this by at least a power of 2. Otherwise, the game ends in a draw.
    3. If there are no more tokens on the board, the game ends in a draw. This may occur due to the stack removal rule (i.e., a single token attacking a POWER 6 opponent token stack, with no other tokens remaining on the board).

In a turn, a player may choose to either:
    1. Spawn a new token in an empty cell, valid only when the power (number of tokens in a token stack) of all cells on the board is less than 49, or
    2. Spread one of their token stacks with the power k, which is defined by the cell's coordinate (r,q) and a hex direction (rd, qd), which is one of the hex neighbour offsets: (0,1), (-1,1), (-1,0), (0,-1), (1,-1), or (1,0). This action leads to the following changes to the board state:
        * All tokens in the chosen token stack are removed from the cell, leaving it empty.
        * The immediately-adjacent line of k cells in the chosen direction, (rd, qd), have one token placed on top of each, thus incrementing their POWER by one.
        * The moving player takes control of any opponent-controlled stacks where a token has been placed on top.

 In the case that a stack is incremented above POWER 6 (the maximum possible power), the stack is completely removed from the game, leaving the cell empty. This also consumes the SPREAD token that would have been placed on top.

## Demo
https://github.com/user-attachments/assets/f0526f62-38e5-4a71-90b4-0f11b3f7f1c7

# Provided Template
search module
1. program.p
•  This contains the method def search(input: dict[tuple, tuple]) -> list[tuple]
  a. input: Python dictionary denoting the initial board state which has entries of the form (r, q): (player, k)
    i. r and q are the coordinates on the board
    ii. player is either "r" (Red) or "b" (Blue)
    ii. k is the power of the cell
  b. list[tuple]: sequence of SPREAD actions wherein each tuple is of the form (r, q, dr, dq) 
    i. r and q represent the original hex position
    ii. dr and dq represent the hex direction of the action which must be one of the following: (0, 1), (−1, 1), (−1, 0), (0, −1), (1, −1), or, (1, 0)

2. __main__.py (Unmodified)
• This contains the input/output code which feeds the solution input and parses the resulting action sequences.

# Commands
## Testing
To test the program against a test case:
    python -m search < test.csv

# Report
## Search Strategy Implementation
For the single player, SPREAD-only version of Infexion, we utilised the A* search strategy to find an optimal solution. Our decision was made by comparing all the uninformed and informed search strategies. The game has a finite number of solutions and each step cost is always equal to 1; hence, only A*, breadth-first search (BFS) and iterative deepening search (IDS) are guaranteed to be complete and optimal out of all the algorithms and were explored. Uniform-cost search also fulfils this criteria, but since it can be reduced to BFS, we decided to disregard it.

For our A* search, we chose data structures that would improve our time and space complexities. The structures are continuously updated as the search progresses:
1. All expanded nodes are stored in a dictionary which takes O(1) time for insertion and lookup.
2. Nodes to expand are stored in a priority queue ordered in ascending f(n) (evaluation function)
values, taking O(n log n) time for enqueue and O(1) for dequeue.

## Time and Space Complexity
In regard to time and space complexities, we define the following terms which are based on the entire search (in other words, while search has not found the optimal solution yet):

● 𝑏: Max. branching factor of search tree; the max. number of possible actions RED can take

● 𝑑: Depth of least cost solution; the min. number of moves to get to the goal state

● ε: Relative error in the heuristic h(𝑛)

Theoretically, A* would perform better than BFS and IDS as long as it uses an admissible heuristic, pruning board states to explore and therefore improving space and time complexity. The performance of
the algorithms would be A* 𝑂(𝑏^(ε𝑑)) < BFS 𝑂(𝑏^𝑑) == IDS 𝑂(𝑏^𝑑) and A* 𝑂(𝑏^(ε𝑑)) < IDS 𝑂(𝑏𝑑) < BFS 𝑂(𝑏^𝑑) based on time and space complexities respectively. Note that A*’s space complexity is 𝑂(𝑏^ε𝑑) since all expanded nodes are kept in memory.

Empirically, A* also had the best performance. As shown in Figure 1, it was able to find a solution in all test cases. The test cases are ordered left to right with ascending difficulty, and while it may appear that BFS stopped after test6-1 and IDS after test6-4, this merely means they had very long running times. While A* initially performed the worst for both time and space complexity, it improved with each level of difficulty, especially over IDS. Though BFS appears to have a better space complexity, the fact that A* is far quicker in finding a solution for more complex boards would indicate that it is still the best choice of search strategy.

<img width="883" alt="Screenshot 2024-01-19 at 6 42 43 pm" src="https://github.com/SiRong-github/shatoria/assets/62817554/983c0d93-18ff-48be-b44a-46ef72e05877">

Figure 1: Results of experiments with A*, IDS, and BFS for test cases of increasing complexity from left to right of the x-axis. Tests can be found in the ‘tests’ folder.

## A* Search Heuristic
Our A* approach uses an evaluation function 𝑓(𝑛) = 𝑔(𝑛) + h(𝑛) where:
● 𝑛 = Board state of interest
● 𝑔(𝑛) = Number of moves to reach board state n
● h(𝑛) = Estimated shortest number of moves to reach a goal state from board state n

To obtain h(𝑛), we assume the board state is in a relaxed version of Infexion and find the shortest number of moves under those conditions. In this version, when we SPREAD a red cell with power p, this directly infects p blue cells on the board in one move and stacks their power by one (they won’t spread over the board as they would in normal Infexion).

Simulating playing n with the steps below intuitively always results in the optimal solution for this relaxed version, avoiding using complex search trees to find the shortest number of moves:
1) Spread the red cell with the highest power to maximise the number of blue cells infected.
2) With the available power the red cell has, infect blue cells with highest powers first so they’ll in
turn have high power as red cells to maximise the number of blue cells infected.
3) Repeat until there are no more blue cells.

<img width="698" alt="Screenshot 2024-01-19 at 6 43 57 pm" src="https://github.com/SiRong-github/shatoria/assets/62817554/70edddf4-311d-4bf1-9a73-083abe3a72a4">

Figure 2: Example of the most optimal move performed in a game of relaxed infexion with the outlined steps. Left board state will go to right board state in one move.

Thus, red cells in this relaxed Infexion will always infect all blue cells in fewer or equal moves than in the real game, making this heuristic admissible and therefore the A* search optimal. Performing A* search with it prunes high-f(n) nodes unlikely to result in optimal solutions early on, reducing both space and time costs of the search as evidenced in Figure 1.

## SPAWN Extension

If SPAWN actions were to be allowed in single player Infexion, this would intuitively cause a goal state to be reached in fewer moves than in the SPREAD-only version, causing d to be slightly smaller. However, b would greatly increase since there are more possible actions a board could do, producing more child nodes when a board state is expanded. Thus, search trees for this version would be larger in width and shorter in height compared to the SPREAD-only counterpart.

This means the heuristic we use for this new problem must prune more nodes at a time to accommodate for the increase in the maximum number of child nodes per expansion. This may require us to devise another heuristic which comes closer to the true cost of getting to the goal state from a board state.
