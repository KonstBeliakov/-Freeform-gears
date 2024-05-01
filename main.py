from perlin_noise import PerlinNoise
import pygame
from math import sin, cos, pi
from time import perf_counter

noiseGenerator = PerlinNoise()
r = 100
height = [r + noiseGenerator(i * 0.05) * 100 for i in range(0, 255)]
k = height[0] / height[-1]
height = [height[i] * (1 + (k - 1) * (i / 255)) for i in range(len(height))]


def position(h, alpha):
    angle = [2 * pi * i / len(h) for i in range(len(h))]
    return [[400 + height[i] * sin(a + alpha), 400 + h[i] * cos(a + alpha)] for i, a in enumerate(angle)]


pygame.init()

size = [800, 800]
screen = pygame.display.set_mode(size)

run = True

t = perf_counter()
t_speed = 0.3

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill([0, 0, 0])
    alpha = (perf_counter() - t) * t_speed
    pos = position(height, -alpha)
    for i in range(len(pos) - 1):
        pygame.draw.line(screen, (255 - i, i, 0), pos[i], pos[i + 1], 1)
    dx = r * alpha

    for i in range(len(height) - 1):
        pygame.draw.line(screen, (0, i, 255), [-dx + 400 + i * (2 * pi * r / 255), 400 + height[i]],
                         [-dx + 400 + i * (2 * pi * r / 255) + 1, 400 + height[i + 1]], 1)

    pygame.display.flip()
pygame.quit()
