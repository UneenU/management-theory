import pygame
from math import *

metr = 1000

class Spring:
    def __init__(self, p1, p2, k, normal_length):
        self.k = k
        self.p1 = p1
        self.p2 = p2
        self.normal_length = normal_length

    def length(self):
        return sqrt((self.p1[0] - self.p2[0])**2 + (self.p1[1] - self.p2[1])**2)

    def draw(self, sc, x0, y0):
        p1 = [self.p1[0] * metr + x0, self.p1[1] * metr + y0]
        p2 = [self.p2[0] * metr + x0, self.p2[1] * metr + y0]
        pygame.draw.line(sc, (10, 10, 100), p1, p2, 10)