# uttt-mcts

Monte Carlo Tree Search implementation for playing Ultimate Tic Tac Toe. School project.

Ultimate Tic Tac Toe is an expanded version of the standard game of Tic Tac Toe. Rules can be found at https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe. The game has proven hard for computers to learn since it lacks a heuristic evaluation function. That means it's hard to determine who is in a better position from some board state. Chess, for example, has such a function. Because of that, I used the MCTS (Monte Carlo Tree Search) algorithm. You can learn more about the algorithm at https://en.wikipedia.org/wiki/Monte_Carlo_tree_search. C_PARAMETER is the exploration vs. exploitation hyperparameter in MCTS. It has been decided empirically from a small sample size, so the values are not guaranteed to be optimal.

The board is numbered like a chess board i.e. horizontally with letters A-I from left to right, and vertically with numbers 1-9 from bottom to top. At startup, the model will first ask for a difficulty. The difficulty represents the number of iterations of the MCTS algorithm. It should be in the tens of thousands for the model to play well. **If the difficulty is under 100, errors can occur!** After the desired difficulty has been inputed, you can simply choose which move to play (e.g. "E5") and the model will respond with the move it wants to make. For now, there is no visual representation of the board in the program itself, and it must be recorded externally.

I have created both a pure-C version and a python version. The C version is faster, but it does not handle errors (yet), so every move must be correctly inputted. The python version, on the other hand, will notify the player when they try to make an illegal move.

Since this is my first big project, and my first real C program, feedback is always welcome.
