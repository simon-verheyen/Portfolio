#
# Holds behavious rf obstacles.
# Obstacles move from right to left on a fixed Y position.
# Holds functions to draw, move, collide and spawn mobstacles.
#

import pygame as pg
import random

START_X = 1300
SMALLEST_HEIGHT = 50
SMALLEST_WIDTH = 25

BASE_SPEED = 10


class Obstacle:
    def __init__(self):
        self.x = START_X
        self.gone = False
        self.y = 0
        self.height = 0
        self.width = 0
        self.type = 'None'

    def move(self):
        self.x -= BASE_SPEED
        if self.x <= - self.width:
            self.gone = True

    def check_collision(self, dino):
        in_rang_x = dino.x + dino.width >= self.x and dino.x <= self.x + self.width
        in_rang_y = dino.y <= self.y + self.height and dino.y + dino.height >= self.y

        return in_rang_x and in_rang_y

    def draw(self, surface):
        pg.draw.rect(surface, (125, 125, 125), (self.x, self.y, self.width, self.height), 0)
        pg.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)


def get_obstacles(i):
    obs_type = random.randint(0, 7)
    obs = []
    if obs_type < 3:
        obs.append(Obstacle())
        obs[i].y = 400
        obs[i].height = SMALLEST_HEIGHT
        obs[i].type = 'small_tree'
        obs[i].width = SMALLEST_WIDTH
        amount = random.randint(0, 1)
        if amount == 1:
            obs.append(Obstacle())
            obs[i + 1].y = 400
            obs[i + 1].height = SMALLEST_HEIGHT
            obs[i + 1].type = 'small_tree'
            obs[i + 1].width = SMALLEST_WIDTH
            obs[i + 1].x += obs[1].width

    elif 3 <= obs_type < 6:
        obs.append(Obstacle())
        obs[i].height = SMALLEST_HEIGHT * 2
        obs[i].type = 'big_tree'
        obs[i].width = SMALLEST_WIDTH * 2
        amount = random.randint(0, 1)
        if amount == 1:
            obs.append(Obstacle())
            obs[i + 1].y = 350
            obs[i + 1].height = SMALLEST_HEIGHT * 2
            obs[i + 1].type = 'big_tree'
            obs[i + 1].width = SMALLEST_WIDTH * 2
            obs[i + 1].x += obs[1].width

    elif 6 <= obs_type < 8:
        obs.append(Obstacle())
        obs[i].y = 350
        obs[i].height = SMALLEST_HEIGHT
        obs[i].width = SMALLEST_WIDTH * 2
        obs[i].type = 'low_bird'

    elif obs_type == 8:
        obs.append(Obstacle())
        obs[i].y = 300
        obs[i].height = SMALLEST_HEIGHT
        obs[i].width = SMALLEST_WIDTH * 2
        obs[i].type = 'high_bird'

    return obs
