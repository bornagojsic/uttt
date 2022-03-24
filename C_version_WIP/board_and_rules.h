#ifndef BOARD_AND_RULES_H
#define BOARD_AND_RULES_H

#include<stdio.h>
#include<string.h>
#include<stdlib.h>

typedef struct Board{ //Game board
	int board[81]; //Game board: -1 cross, 1 circle, 0 empty
	int won[9]; //Which local boards are taken/filled up
} Board;

Board deepcopy_board(Board *board){ //Returns a deepcopy of a Board structure

	Board ret;
	for (int i=0;i<81;++i){
		ret.board[i] = board->board[i];
	}
	for (int i=0;i<9;++i){
		ret.won[i] = board->won[i];
	}
	
	return ret;
}

int **get_legal_moves(Board *board, int move[2]){ //Returns a list of all possible moves from the current board state
	
	int **ret;
	ret = malloc(sizeof(int*) * 81);
	for (int i=0;i<81;++i) ret[i] = malloc(sizeof(int) * 2);
	for (int i=0;i<81;++i){ //Sets all values to -1 to not confuse with move at location 0 (A9)
		for (int j=0;j<2;++j) ret[i][j] = -1;
	}
	int cnt = 0;
	
	if (board->won[move[0] % 9]){ //In case the previous move "sends" the agent to a taken local board
		for (int i=0;i<9;++i){
			if (board->won[i]) continue;
			for (int j=0;j<9;++j){
				if (!board->board[9*i + j]){
					ret[cnt][0] = 9*i + j;
					ret[cnt][1] = (move[1] == -1) ? 1 : -1;
					++cnt;
				}
			}
		}
	}
	
	else{ //Checks only the board that the previous move "sends" to
		int x = move[0] % 9 * 9;
		for (int i=x;i<x+9;++i){
			if (!board->board[i]){
				ret[cnt][0] = i;
				ret[cnt][1] = (move[1] == -1) ? 1 : -1;
				++cnt;
			}
		}
	}
	
	return ret;
}

void update_locals_(Board *board, int move[2]){ //Inplace; checks if the local board the last move "sends" to is taken and updates Board.won
	
	int x = move[0] / 9 * 9;
	for (int i=0;i<7;i+=3){ //Rows
		if (board->board[x+i] == board->board[x+i+1] && board->board[x+i] == board->board[x+i+2] && board->board[x+i] != 0){
			board->won[move[0] / 9] = move[1];
			return;
		}
	}
	for (int i=0;i<3;++i){ //Columns
		if (board->board[x+i] == board->board[x+i+3] && board->board[x+i] == board->board[x+i+6] && board->board[x+i] != 0){
			board->won[move[0] / 9] = move[1];
			return;
		}
	}
	if (board->board[x] == board->board[x+4] && board->board[x] == board->board[x+8] && board->board[x] != 0){ //Main diagonal
		board->won[move[0] / 9] = move[1];
		return;
	}
	else if (board->board[x+2] == board->board[x+4] && board->board[x+2] == board->board[x+6] && board->board[x+2] != 0){ //Secondary diagonal
		board->won[move[0] / 9] = move[1];
		return;
	}
	else{ //If noone won the local board, checks if it is fully filled up
		int flag = 0;
		for (int i=x;i<x+9;++i){
			if (board->board[i]) ++flag;
		}
		if (flag == 9) board->won[move[0] / 9] = -2;
		return;
	}
	
}

int is_terminal(Board *board){ //Checks if the game is over
	
	for (int i=0;i<7;i+=3){ //Rows
		if (board->won[i] == board->won[i+1] && board->won[i] == board->won[i+2] && board->won[i] != 0 && board->won[i] != -2){
			return board->won[i];
		}
	}
	for (int i=0;i<3;++i){ //Columns
		if (board->won[i] == board->won[i+3] && board->won[i] == board->won[i+6] && board->won[i] != 0 && board->won[i] != -2){
			return board->won[i];
		}
	}
	if (board->won[0] == board->won[4] && board->won[0] == board->won[8] && board->won[0] != 0 && board->won[0] != -2){ //Main diagonal
		return board->won[0];
	}
	else if (board->won[2] == board->won[4] && board->won[2] == board->won[6] && board->won[2] != 0 && board->won[2] != -2){ //Secondary diagonal
		return board->won[2];
	}
	int flag = 1; //Tie, all boards are filled up but noone won
	for (int i=0;i<9;++i){
		if (!board->won[i]) flag = 0;
	}
	if (flag){
		return 0;
	}
	
	return -2; //Game is not over
}

void make_move_(Board *board, int move[2]){
	
	board->board[move[0]] = move[1];
	update_locals_(board, move);
	
}

#endif
