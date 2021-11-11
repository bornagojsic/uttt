from Pure_MCTS import GameBoard
from Pure_MCTS import MonteCarlo
from Pure_MCTS import GameRules
from Pure_MCTS import Node
import numpy as np
#Turn characters into integers

class Generate_Data():

    def __init__(self):
        self.X_boards = []
        self.X_wons = []
        self.X = []
        self.Y = []

    def search(self, state, move, difficulty, player):
        mcts = MonteCarlo()
        rules = GameRules()
        mcts.tree = []
        mcts.tree.append(0)
        mcts.tree.append(Node(state, 1, move, children=[]))
        mcts.tree[1].children_moves = rules.get_legal_moves(state, move)
        for diff in range (difficulty):
            nodeind = mcts.selection(mcts.tree[1])
            mcts.expansion(mcts.tree[nodeind])
            if mcts.tree[nodeind].children != []:
                nodeind = mcts.tree[nodeind].children[np.argmax(mcts.UCB1(mcts.tree[nodeind]))]
            result = mcts.simulation(mcts.tree[nodeind])
            mcts.backpropagation(mcts.tree[nodeind], result)
        nodeind = 1
        weights = [mcts.tree[x].wins / mcts.tree[x].visits for x in mcts.tree[nodeind].children]
        if player == 2:
            move = mcts.tree[mcts.tree[nodeind].children[np.argmax(weights)]].parent_move
        elif player == 1:
            move = mcts.tree[mcts.tree[nodeind].children[np.argmin(weights)]].parent_move
        return move

    def play_game(self, diff1, diff2):
        game = GameBoard()
        rules = GameRules()
        move = [40, "x"]
        rules.make_move(game, move)
        while True:
            player = 2
            move = self.search(game, move, diff2, player)
            rules.make_move(game, move)
            rules.is_3x3_taken(game, move)
            self.X_boards.append(game.board)
            self.X_wons.append(game.won)
            if rules.is_game_over(game):
                return rules.is_game_over(game)
            player = 1
            move = self.search(game, move, diff1, player)
            rules.make_move(game, move)
            rules.is_3x3_taken(game, move)
            self.X_boards.append(game.board)
            self.X_wons.append(game.won)
            if rules.is_game_over(game):
                return rules.is_game_over(game)


    def make_data(self):

        diff1 = int(input("Jacina prvog modela: "))
        diff2 = int(input("Jacina drugog modela: "))
        niter = int(input("Broj partija: "))

        for game in range (niter):
            self.X_boards = []
            self.X_wons = []
            result = self.play_game(diff1, diff2)
            for i in range (len(self.X_boards)):
                self.Y.append(result)
            for i in range (len(self.X_wons)):
                temp = []
                for j in range (9):
                    for k in range (9):
                        temp.append(self.X_wons[i][j])
                self.X_wons[i] = temp[:]
            for i in range (len(self.X_boards)):
                self.X.append([self.X_boards[i], self.X_wons[i]])
            self.X = np.array(self.X)
            self.Y = np.array(self.Y)
            np.save("training_data_X.npy", self.X)
            np.save("training_data_Y.npy", self.Y)

execute = Generate_Data()
execute.make_data()    