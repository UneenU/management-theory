import math
from math import *
import random
import pygame
import numpy as np
from matplotlib import pyplot as plt
from Pendulum import Pendulum



# константы
metr = 1000
g = 9.8
FPS = 1000
WIN_WIDTH = 1400
WIN_HEIGHT = 800
WHITE = (255, 255, 255)
ORANGE = (255, 150, 100)
GREEN = (40, 255, 50)
BLACK = (0, 0, 0)

pendulum = Pendulum(-0.2, 0, [0.6, 0.4])



pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
f1 = pygame.font.Font(None, 30)
# ---Главный цикл---
run = True
t = 0
kt = 0
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    dt = clock.get_time() / 1000
    t += dt

    pendulum.base.set_angle(0.5 * sin(t))
    pendulum.base.barrel.set_angle(1*sin(t))

    sc.fill(WHITE)

    pendulum.draw(sc, WIN_WIDTH / 1.5, WIN_HEIGHT / 2)

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

    pygame.display.update()

    clock.tick(FPS)
# ---Закрытие всех модулей Pygame---
pygame.quit()