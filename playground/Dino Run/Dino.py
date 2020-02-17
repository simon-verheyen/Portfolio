#
# Basic Dino behavious.
# Dino's stay on fixed x position and can jump or duck.
#

import pygame as pg
import math

import Brain

JUMP_HEIGHT = 50

START_X = 100
START_Y = 350

DINO_HEIGHT = 100
DINO_WIDTH = 50


class Dino:
    def __init__(self):

        self.x = START_X
        self.y = START_Y
        self.height = DINO_HEIGHT
        self.width = DINO_WIDTH
        self.jump_steps = 0
        self.duck = False
        self.dead = False

        self.brain = Brain.Brain()
        self.score = 0

    def think(self, obs):

        if len(obs) == 1:
            jump, duck = self.brain.to_jump(self.x - obs[0].x, obs[0].y, obs[0].height, obs[0].width, 0,
                                            self.jump_steps)
        else:
            jump, duck = self.brain.to_jump(self.x - obs[0].x, obs[0].y, obs[0].height, obs[0].width,
                                            obs[1].x - obs[0].x, self.jump_steps)

        if duck and self.jump_steps == 0:
            self.duck = True
        elif not duck and self.duck:
            self.duck = False

        if jump and not self.duck:
            self.jump_steps = JUMP_HEIGHT

    def move(self):

        if self.duck:
            self.height = 50
            self.y = 400
        else:
            self.height = 100
            self.y = 350

        if self.jump_steps > 0:
            frac_jump = self.jump_steps / float(JUMP_HEIGHT)
            self.y = START_Y - (1 - math.cos(2 * frac_jump * math.pi)) * self.height
            self.jump_steps -= 1

    def draw(self, surface):
        pg.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        pg.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)
