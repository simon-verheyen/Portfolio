#include "brain.h"

void show_brain(Brain* brain);
Array* think(Brain* brain, Array* input);
void destroy_brain(Brain* brain);

Brain* create_brain(int* dim, int depth);
Layer* create_layer(int size, int size_prev);

void show_brain(Brain* brain) {
	for (int i = 1; i < brain->depth; i++) {
		printf("Layer %i has %i nodes.\n", i, brain->dim[i] + 1);
		for (int j = 0; j < brain->dim[i]; j++){
			printf("Node %i has %i weights.\n", j + 1, brain->layers[i]->weights[j]->size + 1);
			for (int k = 0; k < brain->layers[i]->weights[j]->size; k++) {
				printf("Value of weight %i is %f. \n", k + 1, brain->layers[i]->weights[j]->values[k]);
			}
		}
	}
}

Array* think(Brain* brain, Array* input) {
	Array* a_active = (Array*)malloc(sizeof(Array));
	Array* a_temp = linear_activation_forward(input, brain->layers[0], RELU);
	a_active = a_temp;
	free(a_temp);

	for (int i = 1; i < brain->depth - 1; i++) {
		a_temp = linear_activation_forward(a_active, brain->layers[i], RELU);
		a_active = a_temp;
		free(a_temp);
	}

	a_temp = linear_activation_forward(a_active, brain->layers[brain->depth - 1], SIGMOID);
	a_active = a_temp;

	free(a_temp);
	return a_active;
}

void destroy_brain(Brain* brain) {
	for (int i = 0; i < brain->depth; i++) {
		printf("Layer %i has %i weights.\n", i, brain->dim[i]);
		for (int j = 0; j < brain->dim[i]; j++){
			printf("Node %i has %i weights.\n", j, brain->layers[i]->weights[j]->size);
			for (int k = 0; k < brain->layers[i]->weights[j]->size; k++) {
				printf("Value of weight %i is %f. \n", k, brain->layers[i]->weights[j]->values[k]);
			}
		}
	}
}

Brain* create_brain(int* size, int depth) {
	srand(time(NULL));

	Brain* new_brain = (Brain*)malloc(sizeof(Brain));
	new_brain->depth = depth;
	new_brain->dim = size;
	new_brain->layers = (Layer**)malloc((depth - 1) * sizeof(Layer*));

	for (int i = 1; i < new_brain->depth + 1; i++) {
		new_brain->layers[i] = create_layer(size[i], size[i - 1]);
	}

	return new_brain;
}

Layer* create_layer(int size, int size_prev) {
	Layer* new_layer = (Layer*)malloc(sizeof(Layer));

	new_layer->bias = (Array*)malloc(size * sizeof(Array*));
	new_layer->weights = (Array**)malloc(size_prev * sizeof(Array*));

	new_layer->node_amount = size;
	new_layer->bias = create_zero_array(new_layer->node_amount);

	for (int i = 0; i < new_layer->node_amount; i++) {
		new_layer->weights[i] = create_rand_array(size_prev);
	}

	return new_layer;
}
