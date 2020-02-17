#
# Defines the populations.
# Holds functions to view amount of pop that is alive.
# Holds functions to initiate natural selection within a population by looking at the performance of a pop.
# Performance of a pop is measured by the amount of time they survived.
#

import Dino
import random


def get_deaths(pop):
    life_count = 0

    for d in pop:
        if not d.dead:
            life_count += 1

    return life_count


def get_best(pop):
    best_fitness = 0
    best_ind = 0
    fitness_sum = 0

    for i in range(0, len(pop)):
        fitness_sum += pop[i].score
        if pop[i].score > best_fitness:
            best_fitness = pop[i].score
            best_ind = i

    return pop[best_ind], fitness_sum


def find_parent(pop, fitness_sum):
    rand_sum = int(random.random() * fitness_sum)
    running_sum = 0

    for i in range(0, len(pop)):
        running_sum += pop[i].score
        if running_sum >= rand_sum:
            return pop[i].brain


def natural_selection(pop):
    kids = []
    for i in range(0, len(pop)):
        kids.append(Dino.Dino())

    best_dino, fitness_sum = get_best(pop)
    kids[0].brain.parameters = best_dino.brain.parameters

    for i in range(1, len(kids)):
        mom = find_parent(pop, fitness_sum)
        dad = find_parent(pop, fitness_sum)
        kids[i].brain.parameters = mom.make_baby(dad)
        kids[i].brain.mutate()

    return kids
