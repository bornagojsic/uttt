import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim
from Pure_MCTS import GameBoard, GameRules, Node
from ValueNet import ValueNet
import math

if torch.cuda.is_available():
    Device = torch.device("cpu")
else:
    Device = torch.device("cpu")

Model = ValueNet().double().to(Device)
Model.load_state_dict(torch.load("state_dicts.pt"))

class AlphaBeta():

    def __init__(self):
        self.rules = GameRules()

    def refine_state(self, state):
        ret = np.zeros((1, 4, 81))
        for i in range (81):
            if state.board[i] == "x":
                ret[0][0][i] = 1
            elif state.board[i] == "o":
                ret[0][1][i] = 1
        for i in range (9):
            if state.won[i] == "x":
                for j in range (i*9, i*9+9):
                    ret[0][2][j] = 1
            elif state.won[i] == "o":
                for j in range (i*9, i*9+9):
                    ret[0][3][j] = 1
        return ret

    def evaluation(self, state):
        temp = self.refine_state(state)
        temp = torch.tensor(temp)
        ret = Model(temp).item()
        return ret
    
    def minimax(self, state, move, depth, inv):
        ret = self.rules.is_game_over(state)
        if ret == -2:
            return 0
        elif ret == -1 or ret == 1:
            return inv*ret
        A = []
        children = self.rules.get_legal_moves(state, move)
        if depth == 4:
            return inv*self.evaluation(state)
        for child in children:
            board = state.deepcopy_self()
            self.rules.make_move(board, child)
            self.rules.is_3x3_taken(board, child)
            A.append(inv*self.minimax(board, child, depth+1, -inv))
        if depth == 0:
            return children[np.argmax(A)]
        return max(A)

class Run():

    def __init__(self):
        self.game = GameBoard()
        self.rules = GameRules()
        self.alg = AlphaBeta()

    def play_game(self):
        self.rules.make_move(self.game, [40, "x"])
        self.game.print_board()
        move = self.alg.minimax(self.game, [40, "x"], 0, 1)
        print(move)

test = Run()
test.play_game()
