from math import *
import random
import pygame
import numpy as np

metr = 4400
g = 9.8


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

    def pos_in_win(self, sc: pygame.display):
        return Point(sc.get_width() / 2 + self.x, sc.get_height() / 2 - self.y)


class Gutter:
    def __init__(self, fixed_end: Point, length, angle=0):
        self.fixed_end = fixed_end
        self.length = length
        self.angle = angle
        self.moving_end = Point(fixed_end.x + length * cos(angle),
                                fixed_end.y + length * sin(angle))

    def set_angle(self, angle):
        self.angle = angle
        self.moving_end = Point(self.fixed_end.x + self.length * cos(angle),
                                self.fixed_end.y + self.length * sin(angle))


class Ball:
    def __init__(self, pos_in_gut, radius, mass, gut: Gutter):
        self.radius = radius
        self.mass = mass
        # self.vel = np.array([0., 0.])
        # self.accel = np.array([0., 0.])
        self.vel = 0
        self.accel = 0
        self.pos_in_gut = pos_in_gut
        self.pos = Point(pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                         pos_in_gut * sin(gut.angle) + gut.fixed_end.y)

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
            self.vel = - 0 *self.vel / 1
            self.accel = 0
            self.pos_in_gut = 0
            self.pos = Point(self.pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                             self.pos_in_gut * sin(gut.angle) + gut.fixed_end.y)
        if self.pos_in_gut > gut.length:
            self.vel = - 0 * self.vel / 1
            self.accel = 0
            self.pos_in_gut = gut.length
            self.pos = Point(self.pos_in_gut * cos(gut.angle) + gut.fixed_end.x,
                             self.pos_in_gut * sin(gut.angle) + gut.fixed_end.y)


# константы
FPS = 1000
WIN_WIDTH = 1400
WIN_HEIGHT = 800
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
BLACK = (0, 0, 0)

p0 = Point(0, 0)
# определение желоба
gutter = Gutter(Point(-700, 100), 0.3 * metr, 0)
om = 2
# определение шара
radius = 30
ball = Ball(0, radius, 1, gutter)

# ---Инциализация---
pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# ---Главный игровой цикл---
run = True
k = 0
t = 0
flag = False
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    dt = clock.get_time() / 1000
    t += dt
    print(t)
    if k > 5 and flag or k < -4 and not flag:
        flag = not flag
    if flag:
        k += om * dt
    elif not flag:
        k -= om * dt

    gutter.set_angle(k / 180 * pi)
    ball.update(gutter, dt)

    sc.fill(WHITE)
    # оси координат
    pygame.draw.line(sc, BLACK, (-10000, WIN_HEIGHT / 2),
                     (10000, WIN_HEIGHT / 2))
    pygame.draw.line(sc, BLACK, (WIN_WIDTH / 2, -10000), (WIN_WIDTH / 2, 10000))
    for i in range(-5, 6):
        pygame.draw.circle(sc, BLACK,
                           (WIN_WIDTH / 2 + i * metr, WIN_HEIGHT / 2), 3)
        pygame.draw.circle(sc, BLACK,
                           (WIN_WIDTH / 2, WIN_HEIGHT / 2 + i * metr), 3)
    # желоб и шар
    pygame.draw.line(sc, ORANGE, gutter.fixed_end.pos_in_win(sc).to_tuple(),
                     gutter.moving_end.pos_in_win(sc).to_tuple(), 18)

    pygame.draw.circle(sc, BLACK, ball.pos.pos_in_win(sc).to_tuple(),
                       ball.radius)
    pygame.display.update()

    clock.tick(FPS)
# ---Закрытие всех модулей Pygame---
pygame.quit()
