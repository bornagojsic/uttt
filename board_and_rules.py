from constants import *

class Board():

    def __init__(self):
        self.board = ['.']*81
        self.won = ['.']*9

    def deepcopy_self(self):
        ret = Board()
        ret.board = list(self.board)
        ret.won = list(self.won)

        return ret
    
class GameRules():

    def __init__(self):
        pass

    def get_legal_moves(self, game, move):
        ret = []

        if game.won[move[0] % 9] != '.':
            for i in range (9):
                if game.won[i] != '.':
                    continue
                for j in range (9):
                    if game.board[9*i + j] == '.':
                        position = 9*i + j
                        player = ['o', 'x'][move[1] == 'o']
                        ret.append([position, player])
        
        else:
            x = move[0] % 9 * 9
            for i in range (x, x+9):
                if game.board[i] == '.':
                    position = i
                    player = ['o', 'x'][move[1] == 'o']
                    ret.append([position, player])

        return ret
    
    def is_local_taken_(self, game, local_ind, player):
        x = local_ind * 9
        for i in range (0, 7, 3):
            if game.board[x + i] == game.board[x + i + 1] == game.board[x + i + 2] != '.':
                game.won[local_ind] = player
        for i in range (0, 3):
            if game.board[x + i] == game.board[x + i + 3] == game.board[x + i + 6] != '.':
                game.won[local_ind] = player
        if game.board[x] == game.board[x+4] == game.board[x + 8] != '.':
            game.won[local_ind] = player
        elif game.board[x + 2] == game.board[x + 4] == game.board[x + 6] != '.':
            game.won[local_ind] = player
        else:
            empty = 0
            for i in range (x, x+9):
                if game.board[i] == '.':
                    empty += 1
            if empty == 0:
                game.won[local_ind] = 'f'

    def is_terminal(self, game):
        for i in range (0, 7, 3):
            if game.won[i] == game.won[i + 1] == game.won[i + 2] != '.' and game.won[i] != 'f':
                return game.won[i]
        for i in range (0, 3):
            if game.won[i] == game.won[i + 3] == game.won[i + 6] != '.' and game.won[i] != 'f':
                return game.won[i]
        if game.won[0] == game.won[4] == game.won[8] != '.' and game.won[0] != 'f':
            return game.won[0]
        elif game.won[2] == game.won[4] == game.won[6] != '.' and game.won[2] != 'f':
            return game.won[2]
        elif '.' not in game.won:
            return 't'
        else:
            return '-'

    def make_move_(self, game, move):
        game.board[move[0]] = move[1]
        self.is_local_taken_(game, move[0] // 9, move[1])

class PlayGame(GameRules):

    def __init__(self):
        super().__init__()
        self.game = Board()

    def set_gamestate_(self, gamestate):
        self.game = gamestate.deepcopy_self()

    def input_move(self, prev_player):
        ret = [move_keys[input("Enter your move: ")], ['o', 'x'][prev_player=='o']]
        return ret
    
    def print_board(self):
        print("=============== Board ===============")
        row_inds = [0, 3, 6, 27, 30, 33, 54, 57, 60]
        row_strs = []
        for ind in row_inds:
            row_str = ""
            for i in range (ind, ind+19, 9):
                for j in range (i, i+3):
                    row_str += self.game.board[j]
                row_str += " "
            row_strs.append(row_str)
        for i, row in enumerate(row_strs):
            if i == 3 or i == 6:
                print()
            print(row)
        print("=====================================")

        print("Local boards:", self.game.won)

    def print_legal_moves(self, move):
         print("Legal moves:", [move_keys_inv[x[0]] for x in self.get_legal_moves(self.game, move)])

    def play_game(self, hide_legal_moves=True):
        prev_player = 'x'
        while self.is_terminal(self.game) == '-':
            move = self.input_move(prev_player)
            self.make_move_(self.game, move)
            self.print_board()

            prev_player = ['o', 'x'][prev_player == 'o']
            if not hide_legal_moves:
                self.print_legal_moves(move)

if __name__ == '__main__':
    run = PlayGame()
    run.play_game(hide_legal_moves=False)