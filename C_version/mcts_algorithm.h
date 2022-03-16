#ifndef MCTS_ALGORITHM_H
#define MCTS_ALGORITHM_H

#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"board_and_rules.h"
#include<math.h>

const double C_PARAMETER = 1.7320508075689; //Ecploitation vs. Exploration Hyperparameter, currently set to sqrt(3)
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
		t[cnt] = tree[temp].wins / tree[temp].visits + C_PARAMETER * sqrt(node->visits) / tree[temp].visits;
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
			node = &(tree[node->children[temp-1]]);
			continue;
		}
		break;
	}
	
	return node;
}

#endif