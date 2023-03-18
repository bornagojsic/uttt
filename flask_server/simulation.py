from constants import *
from board_and_rules import Board, GameRules, PlayGame
import random

class Simulation(GameRules):

	def __init__(self):
		super().__init__()

	def get_random_int(self, min, max):
		return int(random.random() * (max-min) + min)

	def random_playout(self, in_gamestate=None, in_prev_move=None):
		if in_gamestate == None:
			gamestate = Board()
			prev_move = [int(random.random() * 80), "o"]
		else:
			gamestate = in_gamestate.deepcopy_self()
			prev_move = in_prev_move[:]
			
		self.make_move_(gamestate, prev_move)

		while self.is_terminal(gamestate) == '-':
			legal_moves = self.get_legal_moves(gamestate, prev_move)
			move = legal_moves[self.get_random_int(0, len(legal_moves))]
			self.make_move_(gamestate, move)
			prev_move = move
		
		return self.is_terminal(gamestate)

	def play_n_randoms(self, num_sims, gamestate=None, prev_move=None):
		results = {"o":0, "x":0, "t":0}

		for _ in range (num_sims):
			if gamestate is not None and prev_move is not None:
				result = self.random_playout(gamestate, prev_move)
			else:
				result = self.random_playout()
			results[result] += 1

		return results

if __name__ == '__main__':
	run = Simulation()
	print(run.play_n_randoms(1000))