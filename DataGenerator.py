from Pure_MCTS import GameBoard
from Pure_MCTS import MonteCarlo
from Pure_MCTS import GameRules
from Pure_MCTS import Node
from tqdm import tqdm
import numpy as np

class Generate_Data():

    def __init__(self):
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
            self.X.append([game.board[:], game.won[:]])
            self.Y.append(-10)
            if rules.is_game_over(game):
                return rules.is_game_over(game)
            player = 1
            move = self.search(game, move, diff1, player)
            rules.make_move(game, move)
            rules.is_3x3_taken(game, move)
            self.X.append([game.board[:], game.won[:]])
            self.Y.append(-10)
            if rules.is_game_over(game):
                return rules.is_game_over(game)


    def make_data(self):
        diff1 = int(input("Jacina prvog modela: "))
        diff2 = int(input("Jacina drugog modela: "))
        games = int(input("Broj partija: "))
        for game in tqdm(range(games)):
            if game % 2 == 0:
                result = self.play_game(diff1, diff2)
            else:
                result = self.play_game(diff2, diff1)
            for i in range (len(self.Y)):
                if self.Y[i] == -10:
                    self.Y[i] = result
            trainX = np.zeros((len(self.X), 4, 81))
            for i in range (len(self.X)):
                for j in range (81):
                    if self.X[i][0][j] == "x":
                        trainX[i][0][j] = 1
                    elif self.X[i][0][j] == "o":
                        trainX[i][1][j] = 1
                for j in range (9):
                    if self.X[i][1][j] == "x":
                        for k in range (j*9, j*9+9):
                            trainX[i][2][k] = 1
                    elif self.X[i][1][j] == "o":
                        for k in range (j*9, j*9+9):
                            trainX[i][3][k] = 1
            trainY = np.zeros(len(self.Y))
            for i in range (len(self.Y)):
                if self.Y[i] == 1:
                    trainY[i] = 1
                elif self.Y[i] == -1:
                    trainY[i] = -1
                elif self.Y[i] == -2:
                    trainY[i] = 0
            p = np.random.permutation(len(trainX))
            trainX = trainX[p]
            trainY = trainY[p]
            np.save("training_data_X.npy", trainX)
            np.save("training_data_Y.npy", trainY)
        
            
            

execute = Generate_Data()
execute.make_data()
