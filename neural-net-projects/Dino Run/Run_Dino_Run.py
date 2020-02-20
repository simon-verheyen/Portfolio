#
# This is the main file of the application.
# Pygame will be initiated and the game loop will run here.
# Creates the population, obstacles.
# creates a new generation and wipes the game field after the active population died out.
#


import pygame as pg
from pygame import *

import Obstacles
import Dino
import Population

FPS = 60

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1300

SCORE_TIMER = USEREVENT
SCORE_INTERVAL = 100

OBSTACLE_SPAWN = USEREVENT + 1
OBSTACLE_INTERVAL = 2000

POPULATION_SIZE = 10


def main():
    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Pygame Flappy Bird')

    clock = pg.time.Clock()

    pg.time.set_timer(OBSTACLE_SPAWN, OBSTACLE_INTERVAL)
    pg.time.set_timer(SCORE_TIMER, SCORE_INTERVAL)

    gen_font = pg.font.SysFont(None, 32, bold=True)

    pop = []
    for i in range(0, POPULATION_SIZE):
        pop.append(Dino.Dino())

    obstacles = []
    amObs = 0
    obstacles.extend(Obstacles.get_obstacles(0))

    gen = 1

    done = paused = False
    while not done:
        for e in pg.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == OBSTACLE_SPAWN:
                obstacles += 1
                obstacles.extend(Obstacles.get_obstacles(amObs))
            elif e.type == SCORE_TIMER:
                for d in pop:
                    if not d.dead:
                        d.score += 1

        clock.tick(FPS)
        if paused:
            continue

        screen.fill((255, 255, 255))

        for d in pop:
            d.think(obstacles)
            d.move()
            if not d.dead:
                d.draw(screen)

        for o in obstacles:
            o.move()
            o.draw(screen)
            if o.gone:
                obstacles.remove(o)
            for d in pop:
                d.dead = o.check_collision(d)

        life_count = Population.get_deaths(pop)
        if life_count != POPULATION_SIZE:
            print(life_count)
        if life_count == 0:
            pop = Population.natural_selection(pop)

            pg.time.set_timer(OBSTACLE_SPAWN, OBSTACLE_INTERVAL)
            pg.time.set_timer(SCORE_TIMER, SCORE_INTERVAL)

            obstacles = []
            amObs = 0
            obstacles.extend(Obstacles.get_obstacles(amObs))
            gen += 1

        gen_surface = gen_font.render('Gen: ' + str(gen), True, (0, 0, 255))
        # score_surface = gens_font.render('Score: ' + str(best_score) + ' Left: ' + str(life_count), True, (0, 0, 255))
        # best_surface = gens_font.render('Best: ' + str(best_total), True, (0, 0, 255))

        screen.blit(gen_surface, (100 - gen_surface.get_width() / 2, 30))
        # screen.blit(score_surface, (490 - score_surface.get_width() / 2, 30))
        # screen.blit(best_surface, (490 - best_surface.get_width() / 2, 30 + score_surface.get_height() + 2))
        pg.draw.line(screen, (0, 0, 0), (0, 450), (1300, 450), 1)

        pg.display.update()

    pg.quit()


main()
