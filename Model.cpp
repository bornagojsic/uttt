#include <bits/stdc++.h>
using namespace std;

map<string, int> move_keys;

int argmax(vector<int> array){
	int maks = array[0];
	int maksind = 0;
	for (int i=0;i<array.size();++i){
		if (array[i] > maks){
			maks = array[i];
			maksind = i;
		}
	}
	return maksind;
}

struct move{
	int ind;
	char sign;
};

class Gameboard{ //Igraca ploca
	
	public:
	
		vector<char> board, won; //won -> koja 3x3 polja su uzeta/popunjena
	
			Gameboard(){
				for (int i=0;i<81;++i){
					board.push_back('.');
				}
				for (int i=0;i<9;++i){
					won.push_back('.');
				}
			}
};

class GameRules{ //Objekt cije metode predstavljaju pravile igre i moguce poteze

	public:
		
		vector<move> get_legal_moves(Gameboard state, move prev_move){ //Vraca listu svih legalnih poteza
			vector<move> legal_moves;
			if (state.won[prev_move.ind % 9] != '.'){ //Ako je 3x3 polje na koje prosli potez salje zauzeto/popunjeno
				for (int i=0;i<9;++i){
					if (state.won[i] != '.') continue;
					for (int j=0;j<9;++j){
						if (state.board[9*i+j] == '.'){
							move tempmove;
							tempmove.ind = 9*i+j;
							tempmove.sign = "xo"[prev_move.sign == 'x'];
							legal_moves.push_back(tempmove);
						}
					}
				}
				return legal_moves;
			}
			int x = prev_move.ind % 9 * 9;
			for (int i=x;i<x+9;++i){ //Standardna provjera 3x3 polja na koje prosli potez salje
				if (state.board[i] == '.'){
					move tempmove;
					tempmove.ind = i;
					tempmove.sign = "xo"[prev_move.sign == 'x'];
					legal_moves.push_back(tempmove); 
				}
			}
			return legal_moves;
		}
		
		void is_3x3_taken(Gameboard &state, move prev_move){ //Inplace; provjerava je li neko 3x3 polje uzeto/popunjeno i sprema u Gameboard.won
			int x = prev_move.ind / 9 * 9;
			if (state.board[x] == state.board[x+1] == state.board[x+2] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+3] == state.board[x+4] == state.board[x+5] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+6] == state.board[x+7] == state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x] == state.board[x+3] == state.board[x+6] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+1] == state.board[x+4] == state.board[x+7] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+2] == state.board[x+5] == state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x] == state.board[x+4] == state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+2] == state.board[x+4] == state.board[x+6] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else{ //Ako nitko nije pobijedio, provjerava je li potpuno popunjeno
				int flag = 0;
				for (int i=x;i<x+9;++i){
					if (state.board[i] != '.') ++flag;
				}
				if (flag == 9){
					state.won[prev_move.ind / 9] = 'w';
				}
			}
		}
	
};

int main(){
ios::sync_with_stdio(0);
cin.tie(0); cout.tie(0);

//Za I/O
move_keys["A9"]=0; move_keys["B9"]=1; move_keys["C9"]=2; move_keys["A8"]=3; move_keys["B8"]=4; move_keys["C8"]=5; move_keys["A7"]=6; move_keys["B7"]=7; move_keys["C7"]=8;
move_keys["D9"]=0; move_keys["E9"]=1; move_keys["F9"]=2; move_keys["D8"]=3; move_keys["E8"]=4; move_keys["F8"]=5; move_keys["D7"]=6; move_keys["E7"]=7; move_keys["F7"]=8;
move_keys["G9"]=0; move_keys["H9"]=1; move_keys["I9"]=2; move_keys["G8"]=3; move_keys["H8"]=4; move_keys["I8"]=5; move_keys["G7"]=6; move_keys["H7"]=7; move_keys["I7"]=8;
move_keys["A6"]=0; move_keys["B6"]=1; move_keys["C6"]=2; move_keys["A5"]=3; move_keys["B5"]=4; move_keys["C5"]=5; move_keys["A4"]=6; move_keys["B4"]=7; move_keys["C4"]=8;
move_keys["D6"]=0; move_keys["E6"]=1; move_keys["F6"]=2; move_keys["D5"]=3; move_keys["E5"]=4; move_keys["F5"]=5; move_keys["D4"]=6; move_keys["E4"]=7; move_keys["F4"]=8;
move_keys["G6"]=0; move_keys["H6"]=1; move_keys["I6"]=2; move_keys["G5"]=3; move_keys["H5"]=4; move_keys["I5"]=5; move_keys["G4"]=6; move_keys["H4"]=7; move_keys["I4"]=8;
move_keys["A3"]=0; move_keys["B3"]=1; move_keys["C3"]=2; move_keys["A2"]=3; move_keys["B2"]=4; move_keys["C2"]=5; move_keys["A1"]=6; move_keys["B1"]=7; move_keys["C1"]=8;
move_keys["D3"]=0; move_keys["E3"]=1; move_keys["F3"]=2; move_keys["D2"]=3; move_keys["E2"]=4; move_keys["F2"]=5; move_keys["D1"]=6; move_keys["E1"]=7; move_keys["F1"]=8;
move_keys["G3"]=0; move_keys["H3"]=1; move_keys["I3"]=2; move_keys["G2"]=3; move_keys["H2"]=4; move_keys["I2"]=5; move_keys["G1"]=6; move_keys["H1"]=7; move_keys["I1"]=8;

Gameboard board;
GameRules rules;
move testmove;
for (int i=0;i<9;++i) cout << board.won[i] << " ";
cout << endl;
testmove.ind = 15;
testmove.sign = 'x';
board.board[9] = 'x';
board.board[12] = 'x';
board.board[15] = 'x';
rules.is_3x3_taken(board, testmove);
for (int i=0;i<9;++i) cout << board.won[i] << " ";

return 0;
}

