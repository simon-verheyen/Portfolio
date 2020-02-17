import Pipe
import Population
import pygame as pg
from pygame.locals import *

FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

POP_SIZE = 50

PIPE_SPAWN = USEREVENT + 1
PIPE_INTERVAL = 3000

FITNESS_TIME = USEREVENT
SECONDS = 100


def main():
    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Pygame Flappy Bird')

    clock = pg.time.Clock()
    gens_font = pg.font.SysFont(None, 32, bold=True)

    population = Population.Pop(POP_SIZE)
    life_count = len(population.pop)

    gen = 1
    best_score = 0
    best_total = 0
    max_score = 1
    pipe_speed = 0

    pg.time.set_timer(PIPE_SPAWN, PIPE_INTERVAL)
    pg.time.set_timer(FITNESS_TIME, SECONDS)

    pipes = []
    pipes.append(Pipe.Pipe())

    done = paused = False
    while not done:
        for e in pg.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == KEYUP and e.key == K_SPACE:
                for b in population.pop:
                    b.alive = False
            elif e.type == PIPE_SPAWN:
                pipes.append(Pipe.Pipe())
                pipe_speed += 1
                pg.time.set_timer(PIPE_SPAWN, int(PIPE_INTERVAL / (1 + pipe_speed / 10)))
            elif e.type == FITNESS_TIME:
                for b in population.pop:
                    b.fitness += 1

        clock.tick(FPS)

        if paused:
            continue

        screen.fill((255, 255, 255))

        if life_count == 0:
            population.natural_selection()

            pg.time.set_timer(PIPE_SPAWN, PIPE_INTERVAL)
            pg.time.set_timer(FITNESS_TIME, SECONDS)

            pipes = []
            pipes.append(Pipe.Pipe())

            best_score = 0
            max_score = 1
            pipe_speed = 0
            gen += 1

        for p in pipes:
            if not p.move(pipe_speed):
                pipes.remove(p)
                max_score += 1
            p.draw(screen)

        for b in population.pop:
            if b.alive:
                b.to_jump(pipes[0])
                b.move()
                b.check_life(pipes[0], max_score)
                b.draw(screen)

                if b.score > best_score:
                    best_score = b.score
                    if best_score > best_total:
                        best_total = best_score

        if population.pop[0].alive:
            population.pop[0].draw_best(screen)

        life_count = population.get_deaths()

        gens_surface = gens_font.render('Gen: ' + str(gen), True, (0, 0, 255))
        score_surface = gens_font.render('Score: ' + str(best_score) + ' Left: ' + str(life_count), True, (0, 0, 255))
        best_surface = gens_font.render('Best: ' + str(best_total), True, (0, 0, 255))

        screen.blit(gens_surface, (100 - gens_surface.get_width() / 2, 30))
        screen.blit(score_surface, (490 - score_surface.get_width() / 2, 30))
        screen.blit(best_surface, (490 - best_surface.get_width() / 2, 30 + score_surface.get_height() + 2))

        pg.display.update()
    pg.quit()


main()
