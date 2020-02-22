# Flappy Birds through Genetic Algoritm

I created rudimentary version of the flappy birds and connected it to a self writen population of neural networks that learn to play the game through a genetic learning algoritm.

The genertic algorithm is implemented by spawning a big group of birds and attributing a fitness score to them depending on how long they survived. 
After which all the fitness scores are added up and a random number is generated within the sum to choose the parents. Meaning that birds that performed badly can still be selected as a parent, with a lower probabilty then the better perfoming ones.

Once the parents are selected, the child is made by taking a random point in the sequence of parameters, slicing both parents at that point and pasting the first part of one parent to the second part of another.
After a child is created a mutation function is called on it, this will ensure that the populations have a change to evolve.


Inspiration: 'Code-Bullet' youtube creator

content:
- Bird.py: Every bird has a brain (nn), as well as position, a fitness on how well it performed (how long it survived) and an option to jump, which is called by the output of the brain every frame. 

- Brain.py: Contains the architecture of the neural networks as well as the compution of processing input and 'deciding' to jump or not as a classification problem. As well as containing the genetic algorithm that creates one child from 2 parent's parameters.

- Pipe.py: Manages the obstacles, pipes, through random position at init and moving every frame towards the birds.

- Popultion.py: Manages the popultion each generation by generating the requested number of birds, comparing their fitness after a trail to find the good parents and creating the children thourgh this for the next generation of birds.

- Start_flapping.py: This is the main script that manages the different trails and resets the gamestate every time a new generation is created.
