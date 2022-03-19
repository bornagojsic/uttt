# uttt-mcts

**WORK IN PROGRESS**

Monte Carlo Tree Search implementation for playing Ultimate Tic Tac Toe. School project.

Ultimate Tic Tac Toe is an expanded version of the standard game of Tic Tac Toe. Rules can be found at https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe. The game has proven hard for computers to learn since it lacks a heuristic evaluation function. That means it's hard to determine who is in a better position from some board state. Chess, for example, has such a function. Techniques like minimax don't accomplish satisfactory results in this game, so I used the MCTS (Monte Carlo Tree Search) algorithm. You can learn more about the algorithm at https://en.wikipedia.org/wiki/Monte_Carlo_tree_search. But, pure MCTS would often surrender local boards early on in the game, which would later cost the model the game against stronger players. For that reason, extra penalization that punishes moves that give the enemy a local board has been implemented. The center board is penalized seperately due to its higher value. The penalties are regulated by the GRIEF_PENALTY parameter. C_PARAMETER is the exploration vs. exploitation hyperparameter in MCTS. Both have been decided empirically from a relatively small sample size, and are not guaranteed to be set at optimal values.

The board is numbered like a chess board i.e. horizontally with letters A-I from left to right, and vertically with numbers 1-9 from bottom to top. At startup, the model will first ask for a difficulty. The difficulty represents the number of iterations of the MCTS algorithm. It should be in the tens of thousands for the model to play well. **If the difficulty is under 100, errors can occur!** After the desired difficulty has been inputed, you can simply choose which move to play (e.g. "E5") and the model will respond with the move it wants to make. 

For now, there is no visual representation of the board in the program itself, and it must be recorded externally.
