from perlin_noise import PerlinNoise
import pygame
from math import sin, cos, pi
from time import perf_counter


def position(h, alpha):
    """
    :param h: list of distances from the center of a figure to points on its surface
    :param alpha: angle of rotation of the figure
    :return: coordinates of points on the surface of a figure relative to its center
    """
    angle = [2 * pi * i / len(h) for i in range(len(h))]
    return [[h[i] * sin(a + alpha), h[i] * cos(a + alpha)] for i, a in enumerate(angle)]


def draw(center_position, screen, pos, alpha, stretch=1.0):
    """
    :param center_position: position of center of rotating figure
    :param screen: pygame screen
    :param pos: coordinates of points on the surface of a figure relative to its center
    :param alpha: rotation angle of the construction
    :param stretch: surface tensile coefficient
    :return: None
    """
    for i in range(len(pos) - 1):
        color = (0, 0, 0)  # (255 - i, i, 0)
        pygame.draw.line(screen, color, [pos[i][0] + center_position[0], pos[i][1] + center_position[1]],
                         [pos[i + 1][0] + center_position[0], pos[i + 1][1] + center_position[1]], 1)
    dx = r * alpha

    for i in range(len(height) - 1):
        color = (0, 0, 0)  # (0, i, 255)
        pygame.draw.line(screen, color, [-dx * stretch + i * stretch * (2 * pi * r / n) + center_position[0], height[i] + center_position[1]],
                         [-dx * stretch + i * stretch * (2 * pi * r / n) + 1 + center_position[0], height[i + 1] + center_position[1]], 1)


noiseGenerator = PerlinNoise()
r = 100
n = 255
height = [r + noiseGenerator(i * 0.05) * 100 for i in range(n)]
k = height[0] / height[-1]
height = [height[i] * (1 + (k - 1) * (i / n)) for i in range(len(height))]

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

    screen.fill([255, 255, 255])
    alpha = (perf_counter() - t) * t_speed
    pos = position(height, -alpha)

    draw([100, 100], screen, pos, alpha,  1.0)

    draw([100, 500], screen, pos, alpha, 1.1)

    pygame.display.flip()
pygame.quit()
