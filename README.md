# uttt-mcts

Monte Carlo Tree Search implementation for playing Ultimate Tic Tac Toe. Personal project.

Ultimate Tic Tac Toe is an expanded version of the standard game of Tic Tac Toe. Rules can be found at https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe. The game has proven hard for computers to learn since it lacks a heuristic evaluation function. That means it's hard to determine who is in a better position from some board state. Chess, for example, has such a function. Because of that, I used the MCTS (Monte Carlo Tree Search) algorithm. You can learn more about the algorithm at https://en.wikipedia.org/wiki/Monte_Carlo_tree_search. C_PARAMETER is the exploration vs. exploitation hyperparameter in MCTS. I have used the default value of sqrt(2). The optimal value should be decided empirically in future experiments.

The board is numbered like a chess board i.e., horizontally with letters A-I from left to right, and vertically with numbers 1-9 from bottom to top. To play versus the AI, simply run the "main.py" program. The human player always has to start first. If you want to change the difficulty, simply increase num_iters. num_sims, which is set to the default value of one, is the number of random rollouts the model will run from each node. This, too, can be increased in order to increase model performance. 

To do:
1. Add toggleable printing of legal moves.
2. Add toggleable printing of model evaluations for possible moves.
3. Do hyperparameter optimisation.
