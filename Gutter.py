from math import *
from Point import Point

class Gutter:
    def __init__(self, fixed_end: Point, length, angle=0):
        self.max_ang_vel = 10 * pi / 180
        self.fixed_end = fixed_end
        self.length = length
        self.angle = angle
        self.moving_end = Point(fixed_end.x + length * cos(angle),
                                fixed_end.y + length * sin(angle))

    def set_angle(self, angle):
        self.angle = angle
        self.moving_end = Point(self.fixed_end.x + self.length * cos(angle),
                                self.fixed_end.y + self.length * sin(angle))