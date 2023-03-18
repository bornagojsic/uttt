from flask import Flask, request
from flask_cors import CORS
from main import PlayVsAI
from constants import *
import os

app = Flask(__name__)
CORS(app)

ai_move = None
## realno ne treba is_over jer ne koristim get request
is_over = None
game_ids = []
games = {}
## hardcodeano
num_iters=1000
num_sims=1


def clear_games():
    global games, game_ids
    if len(games) > 10:
        del games[game_ids[0]]
        game_ids = game_ids[1:]


@app.route('/uttt', methods=['POST', 'GET'])
def handle_move():
    global games, game_ids, move, ai_move, is_over
    if request.method == 'POST':
        game_id = request.json['ID']
        move = request.json['move']
        print(game_id)
        print(move)

        if not game_id in games.keys():
            game_ids.append(game_id)
            games[game_id] = {"game_run": PlayVsAI()}
            clear_games()

        game_run = games[game_id]["game_run"]
        move = game_run.input_move("x", move)
        game_run.make_move_(game_run.game, move)
        game_run.print_board()

        winner = game_run.is_terminal(game_run.game)
        if winner != "-":
            return {'move': '', 'boardWinners': game_run.game.won, 'isOver': winner}

        global move_iters, num_sims, hide_evaluations
        move = game_run.search(game_run.game, move, num_iters, 1, hide_evaluations=True)
        print(move_keys_inv[move[0]])
        game_run.make_move_(game_run.game, move)
        game_run.print_board()

        ai_move = move
        winner = game_run.is_terminal(game_run.game)
        is_over = winner if winner != '-' else 'false'

        return {'move': move_keys_inv[ai_move[0]], 'boardWinners': game_run.game.won, 'isOver': is_over}
        # return {'message': 'move received'}
    elif request.method == 'GET':
        print("\nMOVE:", ai_move)
        print(is_over)
        return {'state': {'move': move_keys_inv[ai_move[0]], 'isOver': is_over}}

if __name__ == '__main__':
    app.run(debug=True)