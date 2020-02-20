#include "brain.h"

void main (){
printf("Hello World!\n");

int size[4] = {1,2,3,1};
int amount_layers = 4;

Brain* brain = (Brain*)malloc(sizeof(Brain));
brain = create_brain(size, amount_layers);
show_brain(brain);
free(brain);
}
