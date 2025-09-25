from math import *
import random
import pygame
import numpy as np

metr = 1000
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


# константы
FPS = 1000
WIN_WIDTH = 1400
WIN_HEIGHT = 800
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
BLACK = (0, 0, 0)

p0 = Point(0, 0)
# определение желоба
gutter = Gutter(Point(-0.5 * metr, 0.0 * metr), 1 * metr, 0)
om = 2
# определение шара
radius = 0.025 * metr
ball = Ball(0, radius, 1, gutter)

# ---Инциализация---
pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
f1 = pygame.font.Font(None, 30)
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
    for i in range(-20, 20):
        s = f1.render(f'{round(i*0.1, 2)}', True, (0, 0, 0))
        sc.blit(s, (WIN_WIDTH / 2 + i * 0.1 * metr, WIN_HEIGHT / 2))
        sc.blit(s, (WIN_WIDTH / 2, WIN_HEIGHT / 2 - i * 0.1 * metr))
        pygame.draw.circle(sc, BLACK,
                           (WIN_WIDTH / 2 + i * 0.1 * metr, WIN_HEIGHT / 2), 3)
        pygame.draw.circle(sc, BLACK,
                           (WIN_WIDTH / 2, WIN_HEIGHT / 2 + i * 0.1 * metr), 3)
    # желоб и шар
    pygame.draw.line(sc, ORANGE, gutter.fixed_end.pos_in_win(sc).to_tuple(),
                     gutter.moving_end.pos_in_win(sc).to_tuple(),
                     int(0.05 * metr))

    pygame.draw.circle(sc, BLACK, ball.pos.pos_in_win(sc).to_tuple(),
                       ball.radius)

    # вывод информации о шаре

    for i in range(3):
        s = f1.render(ball.params()[i], True, (0, 0, 0))
        sc.blit(s, (10, 100+30*i))

    pygame.display.update()

    clock.tick(FPS)
# ---Закрытие всех модулей Pygame---
pygame.quit()
