import math
import random
import copy

move_keys = { #Za I/O
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

def argmax(array): #Argmax funkcija; vraca indeks najvece vrijednosti liste
    maks = array[0]
    maksind = 0
    for i in range (len(array)):
        if array[i] > maks:
            maks = array[i]
            maksind = i
    return maksind

class GameBoard(): #Igraca ploca

    def __init__(self):
        self.board = ["."]*81
        self.won = ["."]*9 #Koja 3x3 polja su uzeta/popunjena

    def print_won(self): #Ispisuje stanje 3x3 polja (won)
        for i in range (3):
            for j in range (3):
                print(self.won[3*i+j], end="")
            print()
    
    def print_board(self): #Ispisuje cijelu plocu
        for k in range (3):
            for l in range (3):
                for i in range (3):
                    for j in range (3):
                        print(self.board[27*k+3*l+9*i+j], end="")
                    print(" ", end="")
                print()
            print()

class GameRules(): #Objekt cije metode predstavljaju pravila igre i moguce poteze

    def get_legal_moves(self, state, prev_move): #Vraca listu svih legalnih poteza
        legal_moves = []
        if state.won[prev_move[0] % 9] != ".": #Ako je 3x3 polje na koje prosli potez salje zauzeto/popunjeno
            for i in range (9):
                if state.won[i] != ".":
                    continue
                for j in range (9):
                    if state.board[9*i+j] == ".":
                        legal_moves.append([9*i+j, ["x", "o"][prev_move[1]=="x"]])
            return legal_moves
        x = prev_move[0] % 9 * 9
        for i in range (x, x+9): #Standardna provejra 3x3 polja na koje prosli potez salje
            if state.board[i] == ".":
                legal_moves.append([i, ["x", "o"][prev_move[1]=="x"]])
        return legal_moves

    def is_3x3_taken(self, state, prev_move): #Inplace; provjerava je li neko 3x3 polje uzeto/popunjeno i sprema u GameBoard.won
        x = prev_move[0] // 9 * 9
        if state.board[x] == state.board[x+1] == state.board[x+2] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x+3] == state.board[x+4] == state.board[x+5] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x+6] == state.board[x+7] == state.board[x+8] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x] == state.board[x+3] == state.board[x+6] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x+1] == state.board[x+4] == state.board[x+7] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x+2] == state.board[x+5] == state.board[x+8] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x] == state.board[x+4] == state.board[x+8] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        elif state.board[x+2] == state.board[x+4] == state.board[x+6] != ".":
            state.won[prev_move[0] // 9] = prev_move[1]
        else: #Ako nitko nije pobijedio, provjerava je li polje potpuno popunjeno
            flag = 0
            for i in range (x, x+9):
                if state.board[i] != ".":
                    flag += 1
            if flag == 9:
                state.won[prev_move[0] // 9] = "w"

    def is_game_over(self, state): #Provjerava je li igra gotova. Ako je, vraca rezultat
        ret = None
        if state.won[0] == state.won[1] == state.won[2] != "." != "w":
            ret = state.won[0]
        elif state.won[3] == state.won[4] == state.won[5] != "." != "w":
            ret = state.won[3]
        elif state.won[6] == state.won[7] == state.won[8] != "." != "w":
            ret = state.won[6]
        elif state.won[0] == state.won[3] == state.won[6] != "." != "w":
            ret = state.won[0]
        elif state.won[1] == state.won[4] == state.won[7] != "." != "w":
            ret = state.won[1]
        elif state.won[2] == state.won[5] == state.won[8] != "." != "w":
            ret = state.won[2]
        elif state.won[0] == state.won[4] == state.won[8] != "." != "w":
            ret = state.won[0]
        elif state.won[2] == state.won[4] == state.won[6] != "." != "w":
            ret = state.won[2]
        else: #Ako nitko nije pobijedio, a sva 3x3 polja su popunjena/zauzeta
            flag = 0
            for i in range (9):
                if state.won[i] != ".":
                    flag += 1
            if flag == 9:
                ret = "w"
        if ret == None: #Igra jos traje
            return 0
        elif ret == "o": #Kruzic je pobijedio
            return 1
        elif ret == "x": #Krizic je pobijedio
            return -1
        else: #Izjednaceno je
            return -2

    def make_move(self, state, move): #Inplace; radi potez na igracoj ploci
        state.board[move[0]] = move[1]

class Node(): #Objekt koji predstavlja cvor u game tree-u

    def __init__(self, state, ind, parent_move, children=[], parent=None, wins=0, visits=0, children_moves=[]):
        self.state = state
        self.ind = ind
        self.parent_move = parent_move
        self.children = children
        self.parent = parent
        self.wins = wins
        self.visits = visits
        self.children_moves = children_moves

class MonteCarlo(): #Metode i komponente MCTS algoritma

    def __init__(self):
        self.rules = GameRules()
        self.tree = [] #Sprema sve cvorove u listu

    def UCB1(self, node, c=2): #Upper Confidence Bound 1, c je hiperparametar exploitation vs. exploration
        ret = []
        for i in node.children:
            temp = self.tree[i]
            if temp.visits == 0:
                ret.append(12345678910) #Ako nije posjeceno dodaj infinity (dijeljenje s nulom)
                continue
            ret.append(temp.wins/temp.visits + c*math.sqrt((math.log(self.tree[temp.parent].visits))/temp.visits))
        return ret

    def selection(self, node): #Bira najbolje dijete trenutnog cvora prema UCB1 i vraca njegov indeks u stablu
        temp = node.ind
        while True:
            if len(self.tree[temp].children_moves):
                return temp
            if len(self.tree[temp].children):
                temp2 = argmax(self.UCB1(self.tree[temp]))
                temp = self.tree[temp].children[temp2]
                continue
            break
        return temp

    def expansion(self, node): #Inplace; prosiruje stablo djecom trenutnog cvora
        if self.rules.is_game_over(node.state):
            return False
        if node.children_moves != []:
            move = node.children_moves.pop()
            board = copy.deepcopy(node.state)
            self.rules.make_move(board, move)
            self.rules.is_3x3_taken(board, move)
            child = Node(board, len(self.tree), move, children=[], parent=node.ind)
            child.children_moves = self.rules.get_legal_moves(child.state, child.parent_move)
            self.tree.append(child)
            node.children.append(child.ind)

    def simulation(self, node): #Simulira nasumicne poteze do kraja igre i vraca rezultat
        board = copy.deepcopy(node.state)
        move = copy.deepcopy(node.parent_move)
        while True:
            if self.rules.is_game_over(board):
                break
            moves = self.rules.get_legal_moves(board, move)
            move = moves[random.randint(0, len(moves)-1)]
            self.rules.make_move(board, move)
            self.rules.is_3x3_taken(board, move)
        return self.rules.is_game_over(board)

    def backpropagation(self, node, result): #Inplace; vraca se unazad po stablu i podesava vrijednosti svih cvorova
        if result > 0: #Pobjeda
            node.wins +=1
        elif result == -2: #Izjednaceno
            node.wins += 0.5
        node.visits += 1
        if node.parent:
            self.backpropagation(self.tree[node.parent], result)

class Run(): #Izvrsavanje programa

    def __init__(self):
        self.rules = GameRules()
        self.game = GameBoard()

    def inputmove(self, prev_sign): #Za laksi unos poteza
        move = input()
        ret = [move_keys[move], ["o", "x"][prev_sign=="o"]]
        return ret

    def search(self, state, move, difficulty): #MCTS algoritam
        mcts = MonteCarlo()
        mcts.tree = []
        mcts.tree.append(0) #Mora poceti od indeksa 1 zbog nekih tehnickih razloga sa boolean vrijednosti nule
        mcts.tree.append(Node(state, 1, move, children=[]))
        mcts.tree[1].children_moves = self.rules.get_legal_moves(state, move)
        for diff in range (difficulty): #MCTS se ponavlja odreden broj puta, veci broj -> bolji AI
            nodeind = mcts.selection(mcts.tree[1])
            mcts.expansion(mcts.tree[nodeind])
            if mcts.tree[nodeind].children != []:
                nodeind = mcts.tree[nodeind].children[argmax(mcts.UCB1(mcts.tree[nodeind]))]
            result = mcts.simulation(mcts.tree[nodeind])
            mcts.backpropagation(mcts.tree[nodeind], result)
        nodeind = 1
        weights = [mcts.tree[x].wins / mcts.tree[x].visits for x in mcts.tree[nodeind].children] #Bira najbolji potez
        move = mcts.tree[mcts.tree[nodeind].children[argmax(weights)]].parent_move
        return move

    def play(self): #Igranje igrice (I/O su potezi oblika A6, B2, ...)
        difficulty = int(input("Odaberite težinu: "))
        prev_sign = "o"
        move = self.inputmove(prev_sign)
        self.rules.make_move(self.game, move)
        while True:
            move = self.search(self.game, move, difficulty)
            for element in move_keys:
                if move_keys[element] == move[0]:
                    print(element)
                    break
            self.rules.make_move(self.game, move)
            self.rules.is_3x3_taken(self.game, move)
            if self.rules.is_game_over(self.game):
                print(move[1], "wins!")
                break
            legal_moves = self.rules.get_legal_moves(self.game, move)
            prev_sign = move[1]
            while True:
                move = self.inputmove(prev_sign)
                if move not in legal_moves:
                    print("Move not legal!")
                    continue
                break
            self.rules.make_move(self.game, move)
            self.rules.is_3x3_taken(self.game, move)
            if self.rules.is_game_over(self.game):
                print(move[1], "wins!")
                break

test = Run()
test.play()
