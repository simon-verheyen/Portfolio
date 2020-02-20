import random
import pygame as pg

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

PIPE_WIDTH = 80
PIPE_SPEED = 3


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = PIPE_WIDTH

        pipe_mid = random.randint(PIPE_WIDTH * 3, SCREEN_HEIGHT - PIPE_WIDTH * 3)
        self.top = pipe_mid - PIPE_WIDTH
        self.bot = pipe_mid + PIPE_WIDTH

    def draw(self, surface):
        pg.draw.rect(surface, (0, 255, 0), (self.x, 0, self.width, self.top), 0)
        pg.draw.rect(surface, (0, 0, 0), (self.x, 0, self.width, self.top), 1)
        pg.draw.rect(surface, (0, 255, 0), (self.x, self.bot, self.width, SCREEN_HEIGHT - self.bot), 0)
        pg.draw.rect(surface, (0, 0, 0), (self.x, self.bot, self.width, SCREEN_HEIGHT - self.bot), 1)

    def move(self, acc):
        self.x -= PIPE_SPEED * (1 + acc / 10)

        if self.x <= - self.width:
            return False

        return True
