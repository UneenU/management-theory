from Barrel import Barrel
from math import *
import pygame
from Spring import Spring

metr = 1000

class Base:
    def __init__(self, x:float, y:float, size:list[float], angle: float):
        self.width, self.height = size
        self.x = x
        self.y = y
        self.angle = angle
        self.barrel = Barrel(self, x, y, 0.4, 0)
        self.p11 = [self.x - sin(self.angle)*self.height/3,
                    self.y - cos(self.angle)*self.height/3]
        self.p21 = [self.x + sin(self.angle) * self.height / 3,
                    self.y + cos(self.angle) * self.height / 3]
        self.first_spring = Spring(self.p11, self.barrel.p, 10)
        self.second_spring = Spring(self.p21, self.barrel.p, 10)
        a = sqrt((self.p11[0] - self.x)**2 + (self.p11[1] - self.y)**2)
        b = sqrt((self.barrel.p[0] - self.x)**2 + (self.barrel.p[1] - self.y)**2)
        c1 = self.first_spring.length()
        c2 = self.second_spring.length()
        alpha = acos((b**2 + c1**2 - a**2) / (b*c1))
        F1 = (c1 - self.first_spring.normal_length)
        F1_rot = F1 * sin(alpha)

        print(self.x, self.y)

    def set_angle(self, angle):
        self.angle = angle
        self.p11 = [self.x - sin(self.angle) * self.height / 3,
                    self.y - cos(self.angle) * self.height / 3]
        self.p21 = [self.x + sin(self.angle) * self.height / 3,
                    self.y + cos(self.angle) * self.height / 3]
        self.first_spring.p1 = self.p11
        self.second_spring.p1 = self.p21



    def draw(self, sc, x0, y0):
        betta = atan(self.width / self.height)
        l = sqrt(self.width ** 2 + self.height ** 2) / 2
        p11 = [x0 + (self.x - sin(self.angle)*self.height/3) * metr,
               y0 + (self.y - cos(self.angle)*self.height/3) * metr]
        p21 = [x0 + (self.x + sin(self.angle) * self.height / 3) * metr,
               y0 + (self.y + cos(self.angle) * self.height / 3) * metr]
        p1 = [x0 + self.x*metr - sin(self.angle+betta) * l * metr,
              y0 + self.y*metr - cos(self.angle+betta) * l * metr]
        p2 = [p1[0] + self.width * cos(self.angle) * metr,
              p1[1] - self.width * sin(self.angle) * metr]
        p3 = [p2[0] + self.height * sin(self.angle) * metr,
              p2[1] + self.height * cos(self.angle) * metr]
        p4 = [p1[0] + self.height * sin(self.angle) * metr,
              p1[1] + self.height * cos(self.angle) * metr]
        points = [p1, p2, p3, p4]
        pygame.draw.polygon(sc, (100, 100, 100), points)
        pygame.draw.circle(sc, (200, 20, 20), p11, 10)
        pygame.draw.circle(sc, (200, 20, 20), p21, 10)
        self.barrel.draw(sc, x0, y0)
        self.first_spring.draw(sc, x0, y0)
        self.second_spring.draw(sc, x0, y0)


