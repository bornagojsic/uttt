DEPTH = 6

def argmax(array):
    maks = array[0]
    maksind = 0
    for i in range (len(array)):
        if array[i] > maks:
            maks = array[i]
            maksind = i
    return maksind

class Game():

    def __init__(self):

        self.board = [0]*81
        self.won = [0]*9

    def deepcopy_self(self):

        ret = Game()
        ret.board = list(self.board)
        ret.won = list(self.won)
        return ret

    def get_legal_moves(self, move):

        ret = []
        if self.won[move[0] % 9]:
            for i in range (9):
                if self.won[i]:
                    continue
                for j in range (9):
                    if self.board[9*i + j] == 0:
                        ret.append([9*i+j, [-1, 1][move[1]==-1]])
        else:
            x = move[0] % 9 * 9
            for i in range (x, x+9):
                if self.board[i] == 0:
                    ret.append([i, [-1, 1][move[1]==-1]])
        return ret

    def is_local_taken_(self, move):

        x = move[0] // 9 * 9
        for i in range (0, 7, 3):
            if self.board[x+i] == self.board[x+i+1] == self.board[x+i+2] != 0:
                self.won[move[0] // 9] = move[1]
        for i in range (0, 3):
            if self.board[x+i] == self.board[x+i+3] == self.board[x+i+6] != 0:
                self.won[move[0] // 9] = move[1]
        if self.board[x] == self.board[x+4] == self.board[x+8] != 0:
            self.won[move[0] // 9] = move[1]
        elif self.board[x+2] == self.board[x+4] == self.board[x+6] != 0:
            self.won[move[0] // 9] = move[1]
        else:
            flag = 0
            for i in range (x, x+9):
                if self.board[i]:
                    flag += 1
            if flag == 9:
                self.won[move[0] // 9] = -2
    
    def is_terminal(self):
        
        ret = None
        for i in range (0, 7, 3):
            if self.won[i] == self.won[i+1] == self.won[i+2] != 0:
                ret = self.won[i]
        for i in range (0, 3):
            if self.won[i] == self.won[i+3] == self.won[i+6] != 0:
                ret = self.won[i]
        if self.won[0] == self.won[4] == self.won[8] != 0:
            ret = self.won[0]
        elif self.won[2] == self.won[4] == self.won[6] != 0:
            ret = self.won[0]
        elif 0 not in self.won:
            ret = 0
        else:
            ret = -2
        return ret

    def make_move_(self, move):

        self.board[move[0]] = move[1]
        self.is_local_taken_(move)

class Alg(Game):

    def evaluation(self, state):

        locals = []
        for i in range (0, 73, 9):
            if state.won[i // 9] != 0:
                locals.append([state.won[i // 9], 0][state.won[i // 9]==-2])
            else:
                locals.append(self.local_evaluation(state.board[i:i+9]))
        return self.local_evaluation(locals)

    def local_evaluation(self, localb):

        neg = 0
        poz = 0
        pairs = 0
        for i in range (9):
            if localb[i] < 0:
                neg += localb[i]
            elif localb[i] > 0:
                poz += localb[i]
        if localb[0] < 0 and localb[1] < 0: #Line
            pairs += (localb[0] + localb[1])/2
        if localb[1] < 0 and localb[2] < 0:
            pairs += (localb[1] + localb[2])/2
        if localb[3] < 0 and localb[4] < 0:
            pairs += (localb[3] + localb[4])/2
        if localb[4] < 0 and localb[5] < 0:
            pairs += (localb[4] + localb[5])/2
        if localb[6] < 0 and localb[7] < 0:
            pairs += (localb[6] + localb[7])/2
        if localb[7] < 0 and localb[8] < 0:
            pairs += (localb[7] + localb[8])/2
        if localb[0] < 0 and localb[3] < 0: #Column
            pairs += (localb[0] + localb[3])/2
        if localb[3] < 0 and localb[6] < 0:
            pairs += (localb[3] + localb[6])/2
        if localb[1] < 0 and localb[4] < 0:
            pairs += (localb[1] + localb[4])/2
        if localb[4] < 0 and localb[7] < 0:
            pairs += (localb[4] + localb[7])/2
        if localb[2] < 0 and localb[5] < 0:
            pairs += (localb[2] + localb[5])/2
        if localb[5] < 0 and localb[8] < 0:
            pairs += (localb[5] + localb[8])/2
        if localb[0] < 0 and localb[4] < 0: #Main diagonal
            pairs += (localb[0] + localb[4])/2
        if localb[4] < 0 and localb[8] < 0:
            pairs += (localb[4] + localb[8])/2
        if localb[2] < 0 and localb[4] < 0: #Secondary diagonal
            pairs += (localb[2] + localb[4])/2
        if localb[4] < 0 and localb[6] < 0:
            pairs += (localb[4] + localb[6])/2
        formula = (neg + pairs + (neg - poz))/34
        return formula
        
        

    def minimax(self, state, move, depth, inv):

        if state.is_terminal() != -2:
            return inv * state.is_terminal()
        if depth == DEPTH:
            return inv * self.evaluation(state)
        children = state.get_legal_moves(move)
        A = []
        for child in children:
            state2 = state.deepcopy_self()
            state2.make_move_(child)
            A.append(inv * self.minimax(state2, child, depth+1, -inv))
        if depth == 0:
            return children[argmax(A)]
        return max(A)

class Run(Alg):

    def __init__(self):
        
        self.game = Game()
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

    def inputmove(self, prev_player):

        ret = [self.move_keys[input()], [-1, 1][prev_player==-1]]
        return ret

    def play_game(self):

        prev_player = -1
        move = self.inputmove(prev_player)
        self.game.make_move_(move)
        while True:
            move = self.minimax(self.game, move, 0, 1)
            for element in self.move_keys:
                if self.move_keys[element] == move[0]:
                    print(element)
                    break
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

test = Run()
test.play_game()
