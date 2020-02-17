#include "brain.h"

Array* create_rand_array(int size);
Array* create_zero_array(int size);

Array* linear_activation_forward(Array* a, Layer* w, char act);
Array* linear_forward(Array* a, Layer* w);
Array* sigmoid(Array* z);
Array* relu(Array* z);

Array* create_rand_array(int size) {
	Array* new_array = (Array*)malloc(sizeof(Array));
	new_array->size = size;
	new_array->values = (double*)malloc(new_array->size * sizeof(double));

	for (int i = 0; i < new_array->size; i++) {
		new_array->values[i] = (rand() % 1000 - 500)/ 1000.;
	}

	return new_array;
}

Array* create_zero_array(int size) {
	Array* new_array = (Array*)malloc(sizeof(Array));
	new_array->size = size;
	new_array->values = (double*)malloc(new_array->size * sizeof(double));

	for (int i = 0; i < new_array->size; i++) {
		new_array->values[i] = 0.;
	}

	return new_array;
}

Array* linear_activation_forward(Array* a, Layer* w, char act) {
	Array* z = linear_forward(a, w);
	Array* new_a = (Array*)malloc(sizeof(Array));

	if (act == SIGMOID) {
		new_a = sigmoid(z);
	}
	else if (act == RELU) {
		new_a = relu(z);
	}

	return new_a;
}

Array* linear_forward(Array* a, Layer* w) {
	Array* z = (Array*)malloc(sizeof(Array));
	z->size = w->node_amount;

	for (int i = 0; i < z->size; i++) {
		z->values[i] = 0;
		for (int j = 0; j < a->size; j++) {
			z->values[i] += a->values[j] * w->weights[i]->values[j] + w->bias->values[i];
		}
	}

	free(a);
	return z;
}

Array* sigmoid(Array* z) {
	Array* a = (Array*)malloc(sizeof(Array));
	a->size = z->size;

	for (int i = 0; i < z->size; i++) {
		a->values[i] = 1 / (1 + (1 / exp(z->values[i])));
	}

	free(z);
	return a;
}

Array* relu(Array* z) {
	Array* a = (Array*)malloc(sizeof(Array));
	a->size = z->size;

	for (int i = 0; i < z->size; i++) {
		a->values[i] = MAX(0, z->values[i]);
	}

	free(z);
	return a;
}
