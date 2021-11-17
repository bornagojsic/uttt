import math #GOES INTO INSTALOSS????
import random

C_PARAMETER = 2

def argmax(array):
    maksind = 0
    maks = array[0]
    for i in range (len(array)):
        if array[i] > maks:
            maks = array[i]
            maksind = i
    return maksind

class Game():

    def __init__(self):

        self.board = [0]*81
        self.won = [0]*9
        self.space = [9]*9

    def deepcopy_self(self):

        ret = Game()
        ret.board = list(self.board)
        ret.won = list(self.won)
        return ret

    def get_legal_moves(self, move):

        ret = []
        if self.won[move[0] % 9] != 0:
            for i in range (9):
                if self.won[i] != 0:
                    continue
                for j in range (9):
                    if self.board[9*i+j] == 0:
                        ret.append([9*i+j, [1, -1][move[1]==1]])
        else:
            for i in range (move[0] % 9 * 9, move[0] % 9 * 9 + 9):
                if self.board[i] == 0:
                    ret.append([i, [1,-1][move[1]==1]])
        return ret

    def is_local_taken_(self, move):

        x = move[0] // 9 * 9
        for i in range (0, 7, 3):
            if self.board[x+i] == self.board[x+i+1] == self.board[x+i+2] and self.board[x+i] != 0:
                self.won[move[0] // 9] = move[1]
                return
        for i in range (0, 3):
            if self.board[x+i] == self.board[x+i+3] == self.board[x+i+6] and self.board[x+i] != 0:
                self.won[move[0] // 9] = move[1]
                return
        if self.board[x] == self.board[x+4] == self.board[x+8] and self.board[x] != 0:
            self.won[move[0] // 9] = move[1]
            return
        elif self.board[x+2] == self.board[x+4] == self.board[x+6] and self.board[x+2] != 0:
            self.won[move[0] // 9] = move[1]
            return
        else:
            flag = 0
            for i in range (x, x+9):
                if self.board[i] != 0:
                    flag += 1
            if flag == 9:
                self.won[move[0] // 9] = -2
        
    def is_terminal(self):

        ret = None
        for i in range (0, 7, 3):
            if self.won[i] == self.won[i+1] == self.won[i+2] and self.won[i] != 0:
                ret = self.won[i]
        for i in range (0, 3):
            if self.won[i] == self.won[i+3] == self.won[i+6] and self.won[i] != 0:
                ret = self.won[i]
        if self.won[0] == self.won[4] == self.won[8] and self.won[0] != 0:
            ret = self.won[0]
        elif self.won[2] == self.won[4] == self.won[6] and self.won[2] != 0:
            ret = self.won[2]
        else:
            flag = 0
            for i in range (9):
                if self.won[i] != 0:
                    flag += 1
            if flag == 9:
                ret = -2
        if ret == None:
            return 0
        else:
            return ret

    def make_move_(self, move):

        self.board[move[0]] = move[1]
        self.space[move[0] // 9] -= 1
        self.is_local_taken_(move)

class Node(Game):

    def __init__(self, state, ind, parent, parent_move):

        self.state = state
        self.ind = ind
        self.parent = parent
        self.parent_move = parent_move
        self.children = []
        self.children_moves = state.get_legal_moves(parent_move)
        self.wins = 0
        self.visits = 0

class MCTS(Game):

    def __init__(self):

        self.tree = []

    def UCB1(self, node, c=C_PARAMETER):

        ret = []
        for i in node.children:
            temp = self.tree[i]
            if temp.visits == 0:
                ret.append(123456)
            else:
                ret.append(temp.wins / temp.visits + c*math.sqrt(math.log(node.visits)/temp.visits))
        return ret

    def selection(self, node):

        while True:
            if len(node.children_moves):
                return node
            if len(node.children):
                temp = argmax(self.UCB1(node))
                node = self.tree[node.children[temp]]
                continue
            break
        return node

    def expansion_(self, node):

        if node.state.is_terminal():
            return False
        elif node.children_moves != []:
            move = node.children_moves.pop()
            state = node.state.deepcopy_self()
            state.make_move_(move)
            child = Node(state, len(self.tree), node.ind, move)
            self.tree.append(child)
            node.children.append(child.ind)

    def simulation(self, node):

        state = node.state.deepcopy_self()
        move = [node.parent_move[0], node.parent_move[1]]
        while True:
            if state.is_terminal():
                break
            moves = state.get_legal_moves(move)
            rand_ind = int(random.random() * len(moves))
            move = moves[rand_ind]
            state.make_move_(move)
        return state.is_terminal()

    def backpropagation_(self, node, result):

        if result == -1:
            node.wins += 1
        elif result == -2:
            node.wins += 0.5
        node.visits += 1
        if node.parent:
            self.backpropagation_(self.tree[node.parent], result)

    def search(self, state, move, difficulty):

        self.tree = []
        self.tree.append(0)
        self.tree.append(Node(state, 1, None, move))
        for diff in range (difficulty):
            node = self.selection(self.tree[1])
            self.expansion_(node)
            if node.children != []:
                best = self.UCB1(node)
                node = self.tree[node.children[argmax(best)]]
            result = self.simulation(node)
            self.backpropagation_(node, result)
        node = self.tree[1]
        weights = [self.tree[x].wins / self.tree[x].visits for x in node.children]
        move = self.tree[node.children[argmax(weights)]].parent_move
        return move

class Run(MCTS):

    def __init__(self):

        self.move_keys = {
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

        self.game = Game()

    def inputmove(self, player):

        move = input()
        move = [self.move_keys[move], [1, -1][player==1]]
        return move

    def play(self):

        difficulty = int(input())
        player = -1
        move = self.inputmove(player)
        self.game.make_move_(move)
        while True:
            move = self.search(self.game, move, difficulty)
            for element in self.move_keys:
                if self.move_keys[element] == move[0]:
                    print(element)
                    break
            self.game.make_move_(move)
            if self.game.is_terminal():
                print(move[1], "wins!")
                break
            legal_moves = self.game.get_legal_moves(move)
            player = move[1]
            while True:
                move = self.inputmove(player)
                if move not in legal_moves:
                    print("Move not legal!")
                    continue
                break
            self.game.make_move_(move)
            if self.game.is_terminal():
                print(move[1], "wins!")
                break

test = Run()
test.play()