from constants import *
from board_and_rules import Board, GameRules, PlayGame
from mcts import Node, MCTS

class PlayVsAI(PlayGame, MCTS):

    def __init__(self):
        super().__init__()

    def play_vs_mcts(self, num_iters, num_sims=1, hide_evaluations=True):
        while self.is_terminal(self.game) == "-":
            move = self.input_move("x")
            self.make_move_(self.game, move)
            self.print_board()

            if self.is_terminal(self.game) != "-":
                break

            move = self.search(self.game, move, num_iters, num_sims, hide_evaluations=hide_evaluations)
            print(move_keys_inv[move[0]])
            self.make_move_(self.game, move)
            self.print_board()
        print(self.is_terminal(self.game), "wins!")

if __name__ == '__main__':
    run = PlayVsAI()
    run.play_vs_mcts(10000)
        