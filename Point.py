import pygame

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def to_tuple(self):
        return self.x, self.y

    def pos_in_win(self, sc):
        return Point(sc.get_width() / 2 + self.x, sc.get_height() / 2 - self.y)
