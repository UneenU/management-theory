from math import *
import pygame

metr = 1000


class Barrel:
    def __init__(self, base, x:float, y:float, length:float, angle:float):
        self.base = base
        self.fixed_end = [x, y]
        self.length = length
        self.angle = angle
        self.free_end = [x + length * cos(angle), y + length * sin(angle)]
        self.p = [self.fixed_end[0] + (self.free_end[0] - self.fixed_end[0]) / 3,
               self.fixed_end[1] + (self.free_end[1] - self.fixed_end[1]) / 3]

    def set_angle(self, angle):
        self.angle = angle
        self.p = [self.fixed_end[0] + (self.free_end[0] - self.fixed_end[0]) / 3,
                  self.fixed_end[1] + (self.free_end[1] - self.fixed_end[1]) / 3]
        self.free_end = [self.fixed_end[0] + self.length * cos(angle),
                         self.fixed_end[1] + self.length * sin(angle)]
        self.base.first_spring.p2 = self.p
        self.base.second_spring.p2 = self.p


    def draw(self, sc, x0, y0):
        p1 = [self.fixed_end[0] * metr + x0, self.fixed_end[1] * metr + y0]
        p2 = [self.free_end[0] * metr + x0, self.free_end[1] * metr + y0]
        pygame.draw.line(sc, (55, 40, 40), p1, p2, 30)