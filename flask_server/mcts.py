from constants import *
from board_and_rules import Board, GameRules, PlayGame
from simulation import Simulation
import math

class Node(GameRules):

    def __init__(self, gamestate, parent_move, ind, parent_ind, wins=0, visits=0):
        super().__init__()

        self.gamestate = gamestate.deepcopy_self()
        self.wins = wins
        self.visits = visits
        self.parent_move = parent_move[:]
        self.children = []
        self.children_moves = self.get_legal_moves(self.gamestate, self.parent_move)
        self.player = ["o", "x"][parent_move[1] == "o"]
        self.ind = ind
        self.parent_ind = parent_ind

class MCTS(Simulation):

    def __init__(self):
        super().__init__()
        self.tree = []

    def argmax(self, lst):
        runmax = lst[0]
        maxind = 0
        for i, el in enumerate(lst):
            if el > runmax:
                runmax = el
                maxind = i
        
        return maxind
    
    def create_root_node_(self, gamestate, parent_move):
        self.tree.append(Node(gamestate, parent_move, 0, None))

    def UCB1(self, node):
        ret = [0]*len(node.children)

        for i, tree_ind in enumerate(node.children):
            child = self.tree[tree_ind]
            if child.visits == 0:
                ret[i] = float('inf')
                continue

            if node.player == "x":
                wr = child.wins / child.visits
            else:
                wr = 1 - (child.wins / child.visits)
            
            ret[i] = wr + C_PARAMETER * math.sqrt(math.log(node.visits) / child.visits)

        return ret

    def selection(self, node):
        while True:
            if len(node.children_moves):
                return node
            if len(node.children):
                i = self.argmax(self.UCB1(node))
                node = self.tree[node.children[i]]
                continue
            break
        return node

    def expansion_(self, node):
        if self.is_terminal(node.gamestate) != '-':
            return
        if len(node.children_moves):
            move = node.children_moves.pop()
            gamestate = node.gamestate.deepcopy_self()
            self.make_move_(gamestate, move)
            child = Node(gamestate, move, len(self.tree), node.ind)
            self.tree.append(child)
            node.children.append(child.ind)

    def simulation(self, node, num_sims=1):
        return self.play_n_randoms(num_sims, node.gamestate, node.parent_move)

    def backpropagation_(self, node, result):
        node.wins += result["x"]
        node.visits += sum(result.values())

        if node.parent_ind is None:
            return
        
        self.backpropagation_(self.tree[node.parent_ind], result)

    def print_evaluation(self):
        pass

    def search(self, gamestate, prev_move, num_iters, num_sims=1, hide_evaluations=True):
        self.tree = []
        self.create_root_node_(gamestate, prev_move)
        root = self.tree[0]

        for _ in range(num_iters):
            node = self.selection(root)
            self.expansion_(node)
            if node.children != []:
                node = self.tree[node.children[self.argmax(self.UCB1(node))]]
            result = self.simulation(node, num_sims)
            self.backpropagation_(node, result)

        wght_visits = [self.tree[x].visits for x in root.children]

        if not hide_evaluations:
            self.print_evaluations()

        best_child = self.tree[root.children[self.argmax(wght_visits)]]
        return best_child.parent_move

if __name__ == '__main__':
    run = MCTS()
    printer = PlayGame()

    gamestate = Board()
    parent_move = [40, "o"]
    run.make_move_(gamestate, parent_move)
    printer.set_gamestate_(gamestate)

    print(run.search(gamestate, parent_move, 10000))
    for node in run.tree[0:9]:
        printer.set_gamestate_(node.gamestate)
        printer.print_board()
        print(node.parent_move)