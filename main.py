from perlin_noise import PerlinNoise
import pygame
from math import sin, cos, pi
from time import perf_counter
import image_read
import settings
import tkinter as tk


def position(h, alpha, angles=None):
    """
    :param h: list of distances from the center of a figure to points on its surface
    :param alpha: angle of rotation of the figure
    :param angles:
    :return: coordinates of points on the surface of a figure relative to its center
    """
    if angles is None:
        angles = [2 * pi * i / len(h) for i in range(len(h))]
    return [[h[i] * sin(a + alpha), h[i] * cos(a + alpha)] for i, a in enumerate(angles)]


def draw(center_position, screen, pos, alpha, height, stretch=1.0, angles=None):
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
    dx = settings.r * alpha

    for i in range(len(height) - 1):
        color = (0, 0, 0)  # (0, i, 255)
        if angles is None:
            a = i * (2 * pi / settings.n)
        else:
            a = angles[i]
        pygame.draw.line(screen, color,
                         [-dx * stretch + a * settings.r * stretch + center_position[0], height[i] + center_position[1]],
                         [-dx * stretch + stretch * a * settings.r + 1 + center_position[0], height[i + 1] + center_position[1]],
                         1)


def run():
    random_generated = settings.random_generated
    if random_generated:
        noiseGenerator = PerlinNoise()
        r = settings.r
        n = settings.n
        height = [r + noiseGenerator(i * settings.perlin_noise_params[0]) * settings.perlin_noise_params[1] for i in
                  range(n)]
        k = height[0] / height[-1]
        height = [height[i] * (1 + (k - 1) * (i / n)) for i in range(len(height))]
    else:
        r = image_read.r
        n = len(image_read.angle)

        height = [i[1] for i in image_read.angle]
        angles = [i[0] for i in image_read.angle]

    pygame.init()

    size = settings.screen_size
    screen = pygame.display.set_mode(size)

    run = True

    t = perf_counter()
    t_speed = settings.speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill([255, 255, 255])
        alpha = (perf_counter() - t) * t_speed

        if random_generated:
            pos = position(height, -alpha)
        else:
            pos = position(height, -alpha, angles=angles)

        if random_generated:
            angles = None

        draw([500, 100], screen, pos, alpha, height, 1.0, angles=angles)
        draw([500, 500], screen, pos, alpha, height, 1.1, angles=angles)

        pygame.display.flip()
    pygame.quit()


def apply_settings():
    pass


def change_text():
    apply_settings()
    run()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Settings")

    texts = ['r', 'n', 'speed', 'random generated figure (y/n)', 'k1', 'k2', 'filename']

    entrys_values = ['' for i in range(len(texts))]

    labels = [tk.Label(root, text=text) for text in texts]
    entrys = [tk.Entry(root) for i in range(len(texts))]

    for i in range(len(texts)):
        labels[i].grid(row=i, column=0)
        entrys[i].grid(row=i, column=1)

    button = tk.Button(root, text="Run", command=change_text)
    button.grid(row=len(texts), column=0)

    root.mainloop()
