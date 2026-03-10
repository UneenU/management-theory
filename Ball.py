from Gutter import Gutter
from math import *
from Point import Point

metr = 600
g = 9.8

class Ball:
    def __init__(self, pos_in_gut, radius, mass, gut: Gutter):
        self.radius = radius
        self.mass = mass
        self.vel = 0
        self.accel = 0
        self.pos_in_gut = pos_in_gut
        self.pos = Point(pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                         pos_in_gut * sin(gut.angle) + gut.fixed_end.y)

    def params(self):
        s = [f'ускорение: {self.accel / metr};',
             f'скорость: {self.vel / metr};',
             f'положение в жёлобе: {self.pos_in_gut / metr}']
        return s

    def update(self, gut: Gutter, t):
        global g
        global metr
        self.accel = -g * sin(gut.angle) * metr
        self.vel += t * self.accel
        self.pos_in_gut += self.vel * t + self.accel * t * t / 2
        self.pos = Point(self.pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                         self.pos_in_gut * sin(gut.angle) + gut.fixed_end.y)
        # self.accel = np.array([a*cos(alpha), a*sin(alpha)])
        # pos = np.array([self.pos.x, self.pos.y]) + t * self.vel + t*t/2 * self.accel
        # self.pos = Point(pos[0], pos[1])

        if self.pos_in_gut < 0:
            self.vel = - self.vel / 1.2
            self.pos_in_gut = 0
            self.pos = Point(self.pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                             self.pos_in_gut * sin(gut.angle) + gut.fixed_end.y)
        if self.pos_in_gut > gut.length:
            self.vel = - self.vel / 1.2
            self.pos_in_gut = gut.length
            self.pos = Point(self.pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                             self.pos_in_gut * sin(gut.angle) + gut.fixed_end.y)