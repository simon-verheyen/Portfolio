#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX(a,b) (((a)>(b))?(a):(b))
#define SIGMOID 's'
#define RELU 'r'

typedef struct Array {
	int size;
	double* values;

}Array;

typedef struct Layer {
	int node_amount;
	Array** weights;
	Array* bias;

} Layer;

typedef struct Brain {
	int* dim;
	int depth;
	Layer** layers;

} Brain;


Brain* create_brain(int* size, int amount_layers);
void show_brain(Brain* brain);
void destroy_brain(Brain* brain);

Array* create_rand_array(int size);
Array* create_zero_array(int size);
Array* linear_activation_forward(Array* a, Layer* w, char act);
