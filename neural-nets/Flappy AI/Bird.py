import Brain
import math
import pygame as pg

BIRD_SIZE = 30

BIRD_DROP = 3
BIRD_JUMP = 5
JUMP_HEIGHT = 20


class Bird:
    def __init__(self):

        self.x = 50
        self.y = 300 - int(BIRD_SIZE / 2)
        self.jump_left = 2
        self.size = BIRD_SIZE

        self.alive = True
        self.score = 0
        self.fitness = 0

        self.brain = Brain.Brain()

    def jump(self):

        self.jump_left = JUMP_HEIGHT

    def to_jump(self, pipe):

        jump = self.brain.to_jump(self.x - pipe.x, self.y - pipe.top, self.y - pipe.bot, self.jump_left)

        if jump:
            self.jump()

    def move(self):

        if self.jump_left >= 0:
            frac_jump = self.jump_left / float(JUMP_HEIGHT)
            self.y -= (1 - math.cos(frac_jump * math.pi)) * BIRD_JUMP
            self.jump_left -= 1
        else:
            self.y += BIRD_DROP

    def check_life(self, pipe, max_score):

        death_in_x = self.x + self.size > pipe.x and self.x < pipe.x + pipe.width
        death_in_y = self.y < pipe.top or self.y + self.size > pipe.bot

        if 0 >= self.y - self.size or 600 <= self.y + self.size or (death_in_x and death_in_y):
            self.alive = False

        if pipe.x + pipe.width < self.x and self.alive and self.score < max_score:
            self.score += 1

    def draw(self, surface):

        pg.draw.rect(surface, (255, 0, 0), (self.x, self.y, BIRD_SIZE, BIRD_SIZE), 0)
        pg.draw.rect(surface, (0, 0, 0), (self.x, self.y, BIRD_SIZE, BIRD_SIZE), 1)

    def draw_best(self, surface):

        pg.draw.rect(surface, (255, 100, 100), (self.x, self.y, BIRD_SIZE, BIRD_SIZE), 0)
        pg.draw.rect(surface, (0, 0, 0), (self.x, self.y, BIRD_SIZE, BIRD_SIZE), 1)
