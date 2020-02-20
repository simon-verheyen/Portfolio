# Dino Run Genetic Algoritm

I created rudimentary version of the dino run game from chrome and connected it to a self writen population of neural networks that learn to play the game through a genetic learning algoritm.

The genertic algorithm is implemented by spawning a big group of birds and attributing a fitness score to them depending on how long they survived. 
After which all the fitness scores are added up and a random number is generated within the sum to choose the parents. Meaning that dino's that performed badly can still be selected as a parent, with a lower probabilty then the better perfoming ones.

Once the parents are selected, the child is made by taking a random point in the sequence of parameters, slicing both parents at that point and pasting the first part of one parent to the second part of another.
After a child is created a mutation function is called on it, this will ensure that the populations have a change to evolve.


Inspiration: 'Code-Bullet' youtube creator

content:
- Dino.py: Every dino has a brain (nn), a fitness on how well it performed (how long it survived) and a jump and duck function,, which is called by the output of the brain every frame. 

- Brain.py: Contains the architecture of the neural networks as well as the compution of processing input and 'deciding' to jump or duck as a 2 classification problems. As well as containing the genetic algorithm that creates one child from 2 parent's parameters.

- Obstacles.py: Manages the obstacles, through random position at init and moving every frame towards the dino's.

- Popultion.py: Manages the popultion each generation by generating the requested number of dinos, comparing their fitness after a trail to find the good parents and creating the children thourgh this for the next generation of dinos.

- Run_Dino_Run.py: This is the main script that manages the different trails and resets the gamestate every time a new generation is created.
