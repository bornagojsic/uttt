#ifndef MCTS_ALGORITHM_H
#define MCTS_ALGORITHM_H

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"board_and_rules.h"
#include<math.h>

const double C_PARAMETER = 1.41421356; //Ecploitation vs. Exploration Hyperparameter, currently set to sqrt(2)
const double GRIEF_PENALTY = 0.2; //Penalizes moves that let the enemy take a local board
const double GRIEF_PENALTY_MIDDLE = 0.2; //Seperately penalizes moves that let the enemy take the central local board

typedef struct Node{ //Node in the MCTS game tree
	Board state; //Current state of the board
	int ind; //Index in the tree (the tree is a list)
	int parent_move[2];
	int parent;
	int num_children;
	int children[81]; //The indices of children
	int children_moves_len;
	int **children_moves;
	float wins;
	float visits;
} Node;

int argmax(float *arr, int arr_size){ //Argmax function; returns the index of the largest value in the array

	float maks = arr[1];
	int maksind = 1;
	for (int i=1;i<=arr_size;++i){
		if (arr[i] > maks){
			maks = arr[i];
			maksind = i;
		}
	}
	
	return maksind;
}

float *UCB1(Node *node, Node tree[]){ //Upper Confidence Bound 1
	
	float *t = malloc(sizeof(float) * 81);
	int cnt = 0;
	for (int i=0;i<81;++i){
		int temp = node->children[i];
		if (temp == -1) continue;
		if (!tree[temp].visits){ //If the child isn't visited, the value is inf
			t[cnt] = 123456;
			++cnt;
			continue;
		}
		t[cnt] = tree[temp].wins / tree[temp].visits + C_PARAMETER * sqrt(log(node->visits)/tree[temp].visits);
		++cnt;
	}
	float *ret = malloc(sizeof(float) * (cnt+1));
	for (int i=1;i<=cnt;++i) ret[i] = t[i-1];
	ret[0] = cnt; //First element is the size of the array
	free(t);
	
	return ret;
}

Node *selection(Node *node, Node tree[]){ //"Descends" down the tree according to UCB1 to the best node
	
	while (1){
		if (node->children_moves_len) return node;
		if (node->num_children){
			float *ucb1 = UCB1(node, tree);
			int temp = argmax(ucb1, (int)ucb1[0]);
			free(ucb1);
			node = &tree[node->children[temp-1]];
			continue;
		}
		break;
	}
	
	return node;
}

void expansion_(Node *node, Node tree[]){ //Inplace; expands the node by one child

	Node *child = &tree[tree[0].ind]; //End of the tree
	
	if (is_terminal(&node->state) != -2) return;
	if (node->children_moves_len){
		
		int *move = malloc(sizeof(int) * 2);
		move[0] = node->children_moves[node->children_moves_len - 1][0];
		move[1] = node->children_moves[node->children_moves_len - 1][1];
		
		child->state = deepcopy_board(&node->state);
		make_move_(&child->state, move);
		child->ind = tree[0].ind; //ind of 0th element is the size of the tree
		child->parent = node->ind;
		child->parent_move[0] = move[0]; child->parent_move[1] = move[1];
		child->num_children = 0;
		for (int i=0;i<81;++i) child->children[i] = -1;
		child->children_moves = get_legal_moves(&child->state, move);
		for (int i=0;i<81;++i) if (child->children_moves[i][0] == -1){
			child->children_moves_len = i;
			break;
		}
		child->wins = 0;
		child->visits = 0;
		free(move);
		
		tree[0].ind += 1; 
		node->children[node->num_children] = child->ind;
		node->num_children += 1;
		node->children_moves_len -= 1;
	}
	
}

int simulation(Node *node, Node tree[], int d1){ //!!!!!!!!!!!!!!!!!!!!!!!!! CRASHES HERE

	
	Board board = deepcopy_board(&node->state);
	int *move = malloc(sizeof(int) * 2);
	move[0] = node->parent_move[0]; move[1] = node->parent_move[1];
	int debug_cnt = 0;
	while (1){
		if (is_terminal(&board) != -2){
			free(move);
			break;
		}
		int **moves = get_legal_moves(&board, move);
		int length;
		for (int i=0;i<81;++i){
			if (moves[i][0] == -1){
				length = i;
				break;
			}
		}
		int rnd = (int)((double)rand() / ((double)RAND_MAX + 1) * length);
		move[0] = moves[rnd][0]; move[1] = moves[rnd][1];
		make_move_(&board, move);
		for (int i=0;i<81;++i) free(moves[i]);
		free(moves);
	}
	
	return is_terminal(&board);
}

void backpropagation_(Node *node, Node tree[], int result){
	
	if (result == 1){
		node->wins += 1;
	}
	else if (result == 0){
		node->wins += 0.5;
	}
	node->visits += 1;
	if (node->parent){
		backpropagation_(&tree[node->parent], tree, result);
	}
	
}

void create_zeroth_node(Node tree[]){
	
	tree[0].ind = 2;
	
}

void create_root_node(Board *state, int move[2], Node tree[]){
	
	tree[1].ind = 1;
	tree[1].state = deepcopy_board(state);
	tree[1].parent_move[0] = move[0]; tree[1].parent_move[1] = move[1];
	tree[1].parent = 0;
	tree[1].num_children = 0;
	tree[1].wins = 0;
	tree[1].visits = 0;
	tree[1].children_moves = get_legal_moves(state, tree[1].parent_move);
	for (int i=0;i<81;++i){
		if (tree[1].children_moves[i][0] == -1){
			tree[1].children_moves_len = i;
			break;
		}
	}
	for (int i=0;i<81;++i) tree[1].children[i] = -1;
	
}

void free_the_tree(Node tree[]){
	
	for (int i=1;i<tree[0].ind;++i){
		for (int j=0;j<81;++j) free(tree[i].children_moves[j]);
		free(tree[i].children_moves);
	}
	free(tree);
	
}

int *search(Board *state, int move[2], int difficulty){
	
	Node *tree = malloc(sizeof(Node) * 1000000);
	create_zeroth_node(tree);
	create_root_node(state, move, tree);
	Node *node;
	for (int diff=0;diff<difficulty;++diff){
		node = selection(&tree[1], tree);
		expansion_(node, tree);
		if (node->num_children){
			float *ucb1 = UCB1(node, tree);
			node = &tree[node->children[argmax(ucb1, (int)ucb1[0]) - 1]];
			free(ucb1);
		}
		int result = simulation(node, tree, diff);
		backpropagation_(node, tree, result);
	}
	node = &tree[1];
	float *weights = malloc(sizeof(float) * (node->num_children + 1));
	for (int i=1;i<=node->num_children;++i){
		weights[i] = tree[node->children[i-1]].visits;
		printf("%f ", weights[i]); fflush(stdout);
	}
	printf("\n"); fflush(stdout);
	int *ret = malloc(sizeof(int) * 2);
	ret[0] = tree[node->children[argmax(weights, node->num_children) - 1]].parent_move[0];
	ret[1] = tree[node->children[argmax(weights, node->num_children) - 1]].parent_move[1];
	free(weights);
	free_the_tree(tree);
	
	return ret;
}

#endif