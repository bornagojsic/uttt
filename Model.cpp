#include <bits/stdc++.h>
using namespace std;

map<string, int> move_keys;

int argmax(vector<double> array){
	double maks = array[0];
	int maksind = 0;
	for (int i=0;i<array.size();++i){
		if (array[i] > maks){
			maks = array[i];
			maksind = i;
		}
	}
	return maksind;
}

struct g_move{
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
		
		vector<g_move> get_legal_moves(Gameboard state, g_move prev_move){ //Vraca listu svih legalnih poteza
			vector<g_move> legal_moves;
			if (state.won[prev_move.ind % 9] != '.'){ //Ako je 3x3 polje na koje prosli potez salje zauzeto/popunjeno
				for (int i=0;i<9;++i){
					if (state.won[i] != '.') continue;
					for (int j=0;j<9;++j){
						if (state.board[9*i+j] == '.'){
							g_move tempmove;
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
					g_move tempmove;
					tempmove.ind = i;
					tempmove.sign = "xo"[prev_move.sign == 'x'];
					legal_moves.push_back(tempmove); 
				}
			}
			return legal_moves;
		}
		
		void is_3x3_taken(Gameboard &state, g_move prev_move){ //Inplace; provjerava je li neko 3x3 polje uzeto/popunjeno i sprema u Gameboard.won
			int x = prev_move.ind / 9 * 9;
			if (state.board[x] == state.board[x+1] && state.board[x+1] == state.board[x+2] && state.board[x+2] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+3] == state.board[x+4] && state.board[x+4] == state.board[x+5] && state.board[x+5] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+6] == state.board[x+7] && state.board[x+7] == state.board[x+8] && state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x] == state.board[x+3] && state.board[x+3] == state.board[x+6] && state.board[x+6] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+1] == state.board[x+4] && state.board[x+4] == state.board[x+7] && state.board[x+7] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+2] == state.board[x+5] && state.board[x+5] == state.board[x+8] && state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x] == state.board[x+4] && state.board[x+4] == state.board[x+8] && state.board[x+8] != '.'){
				state.won[prev_move.ind / 9] = prev_move.sign;
			}
			else if (state.board[x+2] == state.board[x+4] && state.board[x+4] == state.board[x+6] && state.board[x+6] != '.'){
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
		
		int is_game_over(Gameboard state){ //Provjerava je li igra gotova. Ako je, vraca rezultat
			char ret = 'n';
			if (state.won[0] == state.won[1] && state.won[1] == state.won[2] && state.won[2] != '.' && state.won[2] != 'w'){
				ret = state.won[0];
			}
			else if (state.won[3] == state.won[4] && state.won[4] == state.won[5] && state.won[5] != '.' && state.won[5] != 'w'){
				ret = state.won[3];
			}
			else if (state.won[6] == state.won[7] && state.won[7] == state.won[8] && state.won[8] != '.' && state.won[8] != 'w'){
				ret = state.won[6];
			}
			else if (state.won[0] == state.won[3] && state.won[3] == state.won[6] && state.won[6] != '.' && state.won[6] != 'w'){
				ret = state.won[0];
			}
			else if (state.won[1] == state.won[4] && state.won[4] == state.won[7] && state.won[7] != '.' && state.won[7] != 'w'){
				ret = state.won[1];
			}
			else if (state.won[2] == state.won[5] && state.won[5] == state.won[8] && state.won[8] != '.' && state.won[8] != 'w'){
				ret = state.won[2];
			}
			else if (state.won[0] == state.won[4] && state.won[4] == state.won[8] && state.won[8] != '.' && state.won[8] != 'w'){
				ret = state.won[0];
			}
			else if (state.won[2] == state.won[4] && state.won[4] == state.won[6] && state.won[6] != '.' && state.won[6] != 'w'){
				ret = state.won[2];
			}
			else{ //Ako nitko nije pobijedio, a sva 3x3 polja su popunjena zauzeta
				int flag = 0;
				for (int i=0;i<9;++i){
					if (state.won[i] != '.') ++flag;
				}
				if (flag == 9) ret = 'w';
			}
			if (ret == 'n') return 0; //Igra jos traje
			else if (ret == 'o') return 1; //Kruzic je pobijedio
			else if (ret == 'x') return -1; //Krizic je pobijedio
			else return -2; //Izjednaceno je
		}
		
		void make_move(Gameboard &state, g_move potez){
			state.board[potez.ind] = potez.sign;
		}
	
};

class Node{ //Objekt koji predstavlja cvor u game tree-u
	
	public:
		
		Gameboard state;
		int ind;
		g_move parent_move;
		vector<int> children;
		int parent;
		int wins;
		int visits;
		vector<g_move> children_moves;
		
		Node(Gameboard a, int indeks, g_move parentalni_potez, int roditelj){
			state = a;
			ind = indeks;
			parent_move = parentalni_potez;
			parent = roditelj;
			wins = 0;
			visits = 0;
		}
};

Gameboard deepcopy_state(Gameboard state){
	Gameboard ret;
	for (int i=0;i<81;++i) ret.board[i] = state.board[i];
	for (int i=0;i<9;++i) ret.won[i] = state.won[i];
	return ret;
}

class MonteCarlo{ //Metode i komponente MCTS algoritma
	
	public:
		
		GameRules rules;
		vector<Node> tree; //Sprema sve cvorove u listu
		
		vector<double> UCB1(Node node){
			double c = 2; //exploration vs exploitation parametar
			vector<double> ret;
			for (int i=0;i<node.children.size();++i){
				Node temp = tree[i];
				if (temp.visits == 0){
					ret.push_back(1000000); //Ako nije posjeceno dodaj infinity (dijeljenje s nulom)
					continue;
				}
				ret.push_back(temp.wins/temp.visits + c*sqrt((log(tree[temp.parent].visits))/temp.visits));
			}
			return ret;
		}
		
		int selection(Node node){
			int temp = node.ind;
			while (1){
				if (tree[temp].children_moves.size()) return temp;
				if (tree[temp].children.size()){
					int temp2 = argmax(UCB1(tree[temp]));
					temp = tree[temp].children[temp2];
					continue;
				}
				break;
			}
			return temp;
		}
		
		bool expansion(Node node){
			if (rules.is_game_over(node.state)) return false;
			if (node.children_moves.size()){
				g_move potez = node.children_moves[node.children_moves.size()-1]; node.children_moves.pop_back();
				Gameboard board = deepcopy_state(node.state);
				rules.make_move(board, potez);
				rules.is_3x3_taken(board, potez);
				Node child(board, tree.size(), potez, node.ind);
				child.children_moves = rules.get_legal_moves(child.state, child.parent_move);
				tree.push_back(child);
				node.children.push_back(child.ind);
			}
		}
		
		int simulation(Node node){
			Gameboard board = deepcopy_state(node.state);
			g_move potez; potez.ind = node.parent_move.ind; potez.sign = node.parent_move.sign;
			while (1){
				if (rules.is_game_over(board)){
					break;
				}
				vector<g_move> moves = rules.get_legal_moves(board, potez);
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

return 0;
}
