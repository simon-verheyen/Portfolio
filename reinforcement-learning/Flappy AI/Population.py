import Bird
import random


class Pop:
    def __init__(self, size):

        self.pop = []
        self.fitness = 0

        for i in range(0, size):
            self.pop.append(Bird.Bird())

    def get_deaths(self):

        life_count = 0

        for b in self.pop:
            if b.alive:
                life_count += 1

        return life_count

    def get_best(self):

        best_fitness = 0
        best_ind = 0

        for i in range(0, len(self.pop)):
            self.pop[i].fitness += self.pop[i].score * 10000
            self.fitness += self.pop[i].fitness
            if self.pop[i].fitness > best_fitness:
                best_fitness = self.pop[i].fitness
                best_ind = i

        print('Best fitness: ' + str(best_fitness) + ' Ind: ' + str(best_ind))
        print('Total fitness: ' + str(self.fitness))
        return self.pop[best_ind]

    def find_parent(self):

        rand_sum = int(random.random() * self.fitness)
        running_sum = 0

        for i in range(0, len(self.pop)):
            running_sum += self.pop[i].fitness
            if running_sum >= rand_sum:
                return self.pop[i].brain

    def natural_selection(self):

        kids = []
        for i in range(0, len(self.pop)):
            kids.append(Bird.Bird())

        best_bird = self.get_best()
        kids[0].brain.parameters = best_bird.brain.parameters

        for i in range(1, len(kids)):
            mom = self.find_parent()
            dad = self.find_parent()
            kids[i].brain.parameters = mom.make_baby(dad)
            kids[i].brain.mutate()

        self.pop = kids
        self.fitness = 0
