import math
from math import *
import random
import pygame
import numpy as np
from matplotlib import pyplot as plt
from sympy.physics.units import meter

from Gutter import Gutter
from Ball import Ball
from Point import Point
from noises import NoiseGenerator
from Filter import NoiseFilter, KalmanFilter
from PID import PIDController

# константы
metr = 600
g = 9.8
FPS = 100
WIN_WIDTH = 1000
WIN_HEIGHT = 800
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
GREEN = (40, 255, 50)
BLACK = (0, 0, 0)
p0 = Point(0, 0)


# определение желоба
gutter = Gutter(Point(-0.6 * metr, 0.0 * metr), 1.2 * metr, 0)

# определение шара
initial_pos = 0.5
radius = 0.025 * metr
ball = Ball(initial_pos * metr, radius, 1, gutter)

# 0.14 0 0.2 идеально для точного положения
# 0.03 0 0.05 хорошо для шума
# pid_controller = PIDController(gutter, 0.07, 0.0, 0.11)

noise_generator = NoiseGenerator()
noise_filter = NoiseFilter()
kalman_filter = KalmanFilter()

times = []
positions = []
velocities = []
noised_positions = []
filtered_positions = []
angles = []
desired_positions = []

T = 5

# ---Инциализация---
pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
f1 = pygame.font.Font(None, 30)
# ---Главный цикл---
run = True
t = 0
pt = 0
kt = 0
noised_pos = 0
filtered_pos = 0
desired_pos = np.random.rand()
print(desired_pos)
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    dt = clock.get_time() / 1000
    t += dt
    kt += dt
    pt += dt

    U = asin(6*(desired_pos-initial_pos)*(2*pt-T) / g / T**3)
    # обнуление угла при достижении желаемой точки, pt - время от налача управления, dt - время кадра
    if pt + dt > T:
        U = 0
    gutter.set_angle(U)

    ball.update(gutter, dt)

    if pt > T + 3:
        pt = 0
        initial_pos = desired_pos
        desired_pos = np.random.rand()
        print(desired_pos)

    if kt > 0.01:
        # управление через PID

        # noised_pos = noise_generator.add_noise(ball.pos_in_gut / metr)
        # filtered_pos = noise_filter.filter(noised_pos)
        # if (len(filtered_positions) >= 2):
        #     vel = filtered_positions[-1] - filtered_positions[-2]
        # else:
        #     vel = 0
        # accel = -g * sin(gutter.angle)
        # u = vel * dt + accel * dt * dt / 2
        # filtered_pos = kalman_filter(noised_pos, u)
        # pid_controller(filtered_pos, desired_pos, kt)

        times.append(t)
        desired_positions.append(desired_pos)
        angles.append(gutter.angle)
        positions.append(ball.pos_in_gut/metr)
        noised_positions.append(noised_pos)
        filtered_positions.append(filtered_pos)
        velocities.append(ball.vel/metr)
        kt = 0

    sc.fill(WHITE)
    # желоб и шар
    pygame.draw.line(sc, ORANGE, gutter.fixed_end.pos_in_win(sc).to_tuple(),
                     gutter.moving_end.pos_in_win(sc).to_tuple(),
                     int(0.05 * metr))

    pygame.draw.circle(sc, BLACK, ball.pos.pos_in_win(sc).to_tuple(),
                       ball.radius)
    bpos = Point(filtered_pos * metr * cos(gutter.angle) + gutter.fixed_end.x,
                 filtered_pos * metr * sin(gutter.angle) + gutter.fixed_end.y)
    pygame.draw.circle(sc, GREEN, bpos.pos_in_win(sc).to_tuple(),
                       ball.radius)
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

    # вывод информации о шаре

    for i in range(3):
        s = f1.render(ball.params()[i], True, (0, 0, 0))
        sc.blit(s, (10, 100+30*i))

    pygame.display.update()

    clock.tick(FPS)
# ---Закрытие всех модулей Pygame---
pygame.quit()
# plt.plot(times, noised_positions, label='noised', ls='--', c='red')
# plt.plot(times, filtered_positions, label='filtered', )
plt.plot(times, desired_positions, label='positions', c='red')
plt.plot(times, positions, label='positions', c='black')
# plt.plot(times, angles)
plt.legend()
plt.grid()
plt.show()
