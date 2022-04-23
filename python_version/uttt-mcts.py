import random
import math

C_PARAMETER = math.sqrt(3) #Exploitation vs. Exploration hyperparamter in UCB1
GRIEF_PENALTY = 0.2 #Penalizes moves that let the enemy take a local board
GRIEF_PENALTY_MIDDLE = 0.2 #Seperately penalizes moves that let the enemy take the central local board

move_keys = { #For I/O
            "A9":0, "B9":1, "C9":2, "A8":3, "B8":4, "C8":5, "A7":6, "B7":7, "C7":8,
            "D9":9, "E9":10, "F9":11, "D8":12, "E8":13, "F8":14, "D7":15, "E7":16, "F7":17,
            "G9":18, "H9":19, "I9":20, "G8":21, "H8":22, "I8":23, "G7":24, "H7":25, "I7":26,
            "A6":27, "B6":28, "C6":29, "A5":30, "B5":31, "C5":32, "A4":33, "B4":34, "C4":35,
            "D6":36, "E6":37, "F6":38, "D5":39, "E5":40, "F5":41, "D4":42, "E4":43, "F4":44,
            "G6":45, "H6":46, "I6":47, "G5":48, "H5":49, "I5":50, "G4":51, "H4":52, "I4":53,
            "A3":54, "B3":55, "C3":56, "A2":57, "B2":58, "C2":59, "A1":60, "B1":61, "C1":62,
            "D3":63, "E3":64, "F3":65, "D2":66, "E2":67, "F2":68, "D1":69, "E1":70, "F1":71,
            "G3":72, "H3":73, "I3":74, "G2":75, "H2":76, "I2":77, "G1":78, "H1":79, "I1":80
        }

move_keys_inv = {v: k for k, v in move_keys.items()} #Inverse dict of move_keys

def argmax(array): #Argmax function; returns the index of the largest value in the array
    maks = array[0]
    maksind = 0
    for i in range (len(array)):
        if array[i] > maks:
            maks = array[i]
            maksind = i
    return maksind

class Game(): #Game board and game rules

    def __init__(self):

        self.board = [0]*81 #Game board: -1 cross, 1 circle, 0 empty
        self.won = [0]*9 #Which local boards are taken/filled up

    def deepcopy_self(self): #Returns a deepcopy of itself

        ret = Game()
        ret.board = list(self.board)
        ret.won = list(self.won)
        return ret

    def get_legal_moves(self, move): #Returns a list of all possible moves from the current board state

        ret = []
        if self.won[move[0] % 9]: #In case the previous moves "sends" the agent to a taken local board.
            for i in range (9):
                if self.won[i]:
                    continue
                for j in range (9):
                    if self.board[9*i + j] == 0:
                        ret.append([9*i+j, [-1, 1][move[1]==-1]])
        else: #Checks only the board that the previous move "sends" to
            x = move[0] % 9 * 9
            for i in range (x, x+9):
                if self.board[i] == 0:
                    ret.append([i, [-1, 1][move[1]==-1]])
        return ret

    def is_local_taken_(self, move): #Inplace; checks if any local boards are won and updates self.won

        x = move[0] // 9 * 9
        for i in range (0, 7, 3): #Rows
            if self.board[x+i] == self.board[x+i+1] == self.board[x+i+2] != 0:
                self.won[move[0] // 9] = move[1]
        for i in range (0, 3): #Columns
            if self.board[x+i] == self.board[x+i+3] == self.board[x+i+6] != 0:
                self.won[move[0] // 9] = move[1]
        if self.board[x] == self.board[x+4] == self.board[x+8] != 0: #Main diagonal
            self.won[move[0] // 9] = move[1]
        elif self.board[x+2] == self.board[x+4] == self.board[x+6] != 0: #Secondary diagonal
            self.won[move[0] // 9] = move[1]
        else: #If noone won the local board, checks if it is fully filled up
            flag = 0
            for i in range (x, x+9):
                if self.board[i]:
                    flag += 1
            if flag == 9:
                self.won[move[0] // 9] = -2
    
    def is_terminal(self): #Checks if the game is over 
        
        ret = None
        for i in range (0, 7, 3): #Rows
            if self.won[i] == self.won[i+1] == self.won[i+2] and self.won[i] != 0 and self.won[i] != -2:
                ret = self.won[i]
                return ret
        for i in range (0, 3): #Columns
            if self.won[i] == self.won[i+3] == self.won[i+6] and self.won[i] != 0 and self.won[i] != -2:
                ret = self.won[i]
                return ret
        if self.won[0] == self.won[4] == self.won[8] and self.won[0] != 0 and self.won[0] != -2: #Main diagonal
            ret = self.won[0]
            return ret
        elif self.won[2] == self.won[4] == self.won[6] and self.won[2] != 0 and self.won[2] != -2: #Secondary diagonal
            ret = self.won[2]
            return ret
        elif 0 not in self.won: #All local boards won/filled up, but noone won - tie
            ret = 0
            return ret
        else: #Game is not over
            ret = -2
        return ret

    def make_move_(self, move): #Inplace; makes the desired move

        self.board[move[0]] = move[1]
        self.is_local_taken_(move)

class Node(): #Node in the MCTS game tree

    def __init__(self, state, ind, parent_move, parent):

        self.state = state #Current state
        self.ind = ind #Index in the tree (the tree is a list)
        self.parent_move = parent_move 
        self.parent = parent
        self.children = [] #The indices of children
        self.children_moves = self.state.get_legal_moves(self.parent_move)
        self.wins = 0
        self.visits = 0

class MCTS(Game): #Monte Carlo Tree Search Algorithm

    def __init__(self):

        self.tree = [] #MCTS game tree

    def UCB1(self, node, c=C_PARAMETER): #Upper Confidence Bound 1

        ret = []
        for i in node.children:
            temp = self.tree[i]
            if temp.visits == 0: #If it isn't visited, the value is inf
                ret.append(123456)
                continue
            ret.append(temp.wins / temp.visits + c*(math.sqrt(node.visits)/temp.visits))
        return ret

    def selection(self, node): #"Descends" down the tree according to UCB1 to the best node

        while True:
            if len(node.children_moves):
                return node
            if len(node.children):
                temp = argmax(self.UCB1(node))
                node = self.tree[node.children[temp]]
                continue
            break
        return node

    def expansion_(self, node): #Inplace; expands the node by one child

        if node.state.is_terminal() != -2:
            return False
        if node.children_moves != []:
            move = node.children_moves.pop()
            board = node.state.deepcopy_self()
            board.make_move_(move)
            child = Node(board, len(self.tree), move, node.ind)
            self.tree.append(child)
            node.children.append(child.ind)

    def simulation(self, node): #Simulates random moves until the end of the game and returns the result (simulated game isn't recorded anywhere)

        board = node.state.deepcopy_self()
        move = [node.parent_move[0], node.parent_move[1]]
        while True:
            if board.is_terminal() != -2:
                break
            moves = board.get_legal_moves(move)
            randint = int(random.random()*len(moves))
            move = moves[randint]
            board.make_move_(move)
        return board.is_terminal()

    def backpropagation_(self, node, result): #Inplace; modifies the values of the nodes with respect to the result of the simulation

        if result == 1: #Circle (Model) won
            node.wins += 1
        elif result == 0: #Tie
            node.wins += 0.5
        node.visits += 1
        if node.parent:
            self.backpropagation_(self.tree[node.parent], result)

    def punish_grief_(self, weights, node): #Punishes bad moves (check README)

        for i in range(len(node.children)):
            child = self.tree[node.children[i]]
            current = child.state.won.count(-1) #Current number of local boards the enemy has
            for gc_ind in child.children:
                grandchild = self.tree[gc_ind]
                if grandchild.state.is_terminal() == -1: #If the enemy can win next move, don't play this
                    weights[i] = 0
                    break
                if grandchild.state.won[4] == -1 and child.state.won[4] != -1: #Punishes a move that lets the enemy take the center local board
                    weights[i] -= GRIEF_PENALTY_MIDDLE*weights[i]
                    break
                future = grandchild.state.won.count(-1) 
                if future > current: #Punishes a move that lets the enemy take some local board (not center)
                    weights[i] -= GRIEF_PENALTY*weights[i]
                    break

    def search(self, state, move, difficulty): #Finds the best move from some game state - MCTS algorithm

        self.tree = []
        self.tree.append(0) #Filler; Root node must be at index 1 because of "if parent" in backpropagation_
        first_node = Node(state, 1, move, 0)
        self.tree.append(first_node)
        for diff in range (difficulty): #More iterations -> better model
            node = self.selection(self.tree[1])
            self.expansion_(node)
            if node.children != []:
                node = self.tree[node.children[argmax(self.UCB1(node))]]
            result = self.simulation(node)
            self.backpropagation_(node, result)
        node = self.tree[1]
        weights = [self.tree[x].visits for x in node.children] #Selects the most visited child
        self.punish_grief_(weights, node)
        for i in range(len(weights)): #Prints how "good" each move is
            print(move_keys_inv[self.tree[node.children[i]].parent_move[0]], weights[i])
        move = self.tree[node.children[argmax(weights)]].parent_move
        return move


class Run(MCTS):

    def __init__(self):
        
        self.game = Game()

    def inputmove(self, prev_player): #Turns e.g. A8 into a representation of the move in the program [3, 1] (index, player)

        ret = [move_keys[input()], [-1, 1][prev_player==-1]]
        return ret

    def play_game(self): #Game playing

        difficulty = int(input())
        prev_player = 1
        move = self.inputmove(prev_player)
        self.game.make_move_(move)
        while True:
            move = self.search(self.game, move, difficulty)
            print(move_keys_inv[move[0]])
            self.game.make_move_(move)
            if self.game.is_terminal() != -2:
                print(self.game.is_terminal(), "wins!")
            legal_moves = self.game.get_legal_moves(move)
            prev_player = move[1]
            while True:
                move = self.inputmove(prev_player)
                if move not in legal_moves:
                    print("Move not legal!")
                    continue
                break
            self.game.make_move_(move)
            if self.game.is_terminal() != -2:
                print(self.game.is_terminal(), "wins!")
                break

if __name__ == '__main__':
            test = Run()
            test.play_game()
