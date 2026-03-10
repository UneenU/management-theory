from math import *
import pygame
from Base import Base

metr = 1000


class Pendulum:
    def __init__(self, x: float, y: float, size: list[float]):
        self.pos = [x, y]
        self.size = size
        self.base = Base(0, 0, [0.1, 0.2], 0)

    def draw(self, sc, x0, y0):
        pygame.draw.rect(sc, (100, 80, 90), [self.pos[0]*metr + x0 - self.size[0] / 2 * metr,
                                             self.pos[1]*metr + y0 - self.size[1] / 2 * metr,
                                             self.size[0] * metr, self.size[1] * metr])
        self.base.draw(sc, x0, y0)
