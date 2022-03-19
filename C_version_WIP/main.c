#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"board_and_rules.h"
#include"mcts_algorithm.h"

int *input_move(int prev_player){
	
	char moves[2];
	scanf("%s", &moves);
	int *ret = malloc(sizeof(int) * 2);
	
	int t = (int)(moves[1]) - (int)('0');
	if (moves[0] == 'A' || moves[0] == 'B' || moves[0] == 'C'){
		if (t > 6) ret[0] = (9 - t)*3 + (int)(moves[0]) - (int)('A');
		else if (t > 3) ret[0] = (6 - t)*3 + (int)(moves[0]) - (int)('A') + 27;
		else if (t > 0) ret[0] = (3 - t)*3 + (int)(moves[0]) - (int)('A') + 54;
	}
	else if (moves[0] == 'D' || moves[0] == 'E' || moves[0] == 'F'){
		if (t > 6) ret[0] = (9 - t)*3 + (int)(moves[0]) - (int)('D') + 9;
		else if (t > 3) ret[0] = (6 - t)*3 + (int)(moves[0]) - (int)('D') + 36;
		else if (t > 0) ret[0] = (3 - t)*3 + (int)(moves[0]) - (int)('D') + 63;
	}
	else if (moves[0] == 'G' || moves[0] == 'H' || moves[0] == 'I'){
		if (t > 6) ret[0] = (9 - t)*3 + (int)(moves[0]) - (int)('G') + 18;
		else if (t > 3) ret[0] = (6 - t)*3 + (int)(moves[0]) - (int)('G') + 45;
		else if (t > 0) ret[0] = (3 - t)*3 + (int)(moves[0]) - (int)('G') + 72;
	}
	
	ret[1] = (prev_player == -1) ? 1 : -1;
	
	return ret;
}

void output_move(int move[2]){
	
	char ret;
	int ret2;
	
	if (0 <= move[0] && move[0] <= 8) ret = (char)((int)('A') + (move[0] % 3));	
	else if (9 <= move[0] && move[0] <= 17) ret = (char)((int)('D') + (move[0] % 3));
	else if (18 <= move[0] && move[0] <= 26) ret = (char)((int)('G') + (move[0] % 3));
	else if (27 <= move[0] && move[0] <= 35) ret = (char)((int)('A') + (move[0] % 3));	
	else if (36 <= move[0] && move[0] <= 44) ret = (char)((int)('D') + (move[0] % 3));
	else if (45 <= move[0] && move[0] <= 53) ret = (char)((int)('G') + (move[0] % 3));
	else if (27 <= move[0] && move[0] <= 35) ret = (char)((int)('A') + (move[0] % 3));	
	else if (36 <= move[0] && move[0] <= 44) ret = (char)((int)('D') + (move[0] % 3));
	else if (45 <= move[0] && move[0] <= 53) ret = (char)((int)('G') + (move[0] % 3));
	else if (54 <= move[0] && move[0] <= 62) ret = (char)((int)('A') + (move[0] % 3));	
	else if (63 <= move[0] && move[0] <= 71) ret = (char)((int)('D') + (move[0] % 3));
	else if (72 <= move[0] && move[0] <= 80) ret = (char)((int)('G') + (move[0] % 3));
	
	int t = move[0] / 9;
	if (0 <= t && t <= 2) ret2 = 9 - (move[0] % 9 / 3);
	else if (3 <= t && t <= 5) ret2 = 6 - (move[0] % 9 / 3);
	else if (6 <= t && t <= 8) ret2 = 3 - (move[0] % 9 / 3);
	printf("%c%d\n", ret, ret2); fflush(stdout);
	
}

int main(){
	
	int difficulty;
	Board game;
	for (int i=0;i<81;++i) game.board[i] = 0;
	for (int i=0;i<9;++i) game.board[i] = 0;
	int prev_player = 1;
	
	printf("Hello! Please enter the desired difficulty (cca 50 000 -> decent)\n"); fflush(stdout);
	scanf("%d", &difficulty);
	printf("Let's play. Make your move.\n"); fflush(stdout);
	int *move = input_move(prev_player);
	make_move_(&game, move);
	
	while (1){
		move = search(&game, move, difficulty);
		output_move(move);
		make_move_(&game, move);
		if (is_terminal(&game) != -2){
			printf("%d wins!", move[1]);
			fflush(stdout);
			break;
		}
		prev_player = move[1];
		move = input_move(prev_player);
		make_move_(&game, move);
		if (is_terminal(&game) != -2){
			printf("%d wins!", move[1]);
			fflush(stdout);
			break;
		}
	}
	
	return 0;
}