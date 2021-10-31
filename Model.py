import math
import random
import copy

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

    def __init__(self, state, ind, parent_move, children=[], parent=None, wins=0, visits=0):
        self.state = state
        self.ind = ind
        self.parent_move = parent_move
        self.children = children
        self.parent = parent
        self.wins = wins
        self.visits = visits

class MonteCarlo(): #Metode i komponente MCTS algoritma

    def __init__(self):
        self.rules = GameRules()
        self.tree = [] #Sprema sve cvorove u listu

    def UCB1(self, node, c=1.41): #Upper Confidence Bound 1, c je hiperparametar exploitation vs. exploration
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
            if len(self.tree[temp].children):
                temp2 = argmax(self.UCB1(self.tree[temp]))
                temp = self.tree[temp].children[temp2]
                continue
            break
        return temp

    def expansion(self, node): #Inplace; prosiruje stablo djecom trenutnog cvora
        if self.rules.is_game_over(node.state):
            return False
        moves = self.rules.get_legal_moves(node.state, node.parent_move)
        for move in moves:
            board = copy.deepcopy(node.state)
            self.rules.make_move(board, move)
            self.rules.is_3x3_taken(board, move)
            child = Node(board, len(self.tree), move, children=[], parent=node.ind)
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
        if result > 0:
            node.wins +=1
        node.visits += 1
        if node.parent:
            self.backpropagation(self.tree[node.parent], result)

class Run(): #Izvrsavanje programa

    def __init__(self):
        self.rules = GameRules()
        self.game = GameBoard()

    def inputmove(self): #Za laksi unos poteza
        move = list(input().split())
        move[0] = int(move[0])
        return move

    def search(self, state, move, difficulty): #MCTS algoritam
        mcts = MonteCarlo()
        mcts.tree = []
        mcts.tree.append(0) #Mora poceti od indeksa 1 zbog nekih tehnickih razloga sa boolean vrijednosti nule
        mcts.tree.append(Node(state, 1, move, children=[]))
        for diff in range (difficulty): #MCTS se ponavlja odreden broj puta, veci broj -> bolji AI
            nodeind = mcts.selection(mcts.tree[1])
            mcts.expansion(mcts.tree[nodeind])
            if mcts.tree[nodeind].children != []:
                nodeind = mcts.tree[nodeind].children[0]
            result = mcts.simulation(mcts.tree[nodeind])
            mcts.backpropagation(mcts.tree[nodeind], result)
        nodeind = 1
        weights = [mcts.tree[x].wins / mcts.tree[x].visits for x in mcts.tree[nodeind].children] #Bira najbolji potez
        move = mcts.tree[mcts.tree[nodeind].children[argmax(weights)]].parent_move
        return move

    def play_in_shell(self): #Igra igricu u shellu, zasad ovdje samo za testiranje
        difficulty = int(input("Odaberite tezinu (brojcano): "))
        self.game.print_board()
        move = self.inputmove()
        self.rules.make_move(self.game, move)
        self.game.print_board()
        while True:
            print()
            move = self.search(self.game, move, difficulty)
            self.rules.make_move(self.game, move)
            self.rules.is_3x3_taken(self.game, move)
            self.game.print_board()
            if self.rules.is_game_over(self.game):
                break
            legal_moves = self.rules.get_legal_moves(self.game, move)
            print(legal_moves)
            while True:
                move = self.inputmove()
                if move not in legal_moves:
                    print("Move not legal!")
                    continue
                break
            self.rules.make_move(self.game, move)
            self.game.print_board()
            self.rules.is_3x3_taken(self.game, move)
            if self.rules.is_game_over(self.game):
                break

test = Run()
test.play_in_shell()
