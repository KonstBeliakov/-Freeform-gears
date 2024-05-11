from time import perf_counter

import pygame
from math import pi
from perlin_noise import PerlinNoise

import image_read
import settings
import utils


class MainWindow:
    def __init__(self):
        if settings.random_generated:
            noiseGenerator = PerlinNoise()
            height = [settings.r + noiseGenerator(i * settings.perlin_noise_params[0]) * settings.perlin_noise_params[1]
                      for
                      i in
                      range(settings.n)]
            k = height[0] / height[-1]
            self.height = [height[i] * (1 + (k - 1) * (i / settings.n)) for i in range(len(height))]
            self.angles = None
        else:
            settings.r = settings.r
            settings.n = len(image_read.angle)

            self.height = [i[1] for i in image_read.angle]
            self.angles = [i[0] for i in image_read.angle]

        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.t = perf_counter()
        self.t_speed = settings.speed

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(settings.background_color)
        alpha = (perf_counter() - self.t) * self.t_speed

        pos1 = utils.position(self.height, 0, angles=self.angles)
        pos2 = utils.position(self.height, -alpha, angles=self.angles)

        if settings.random_generated:
            angles = None

        l = settings.r * settings.surface_stretching * pi * 2

        utils.draw_surface([50, 100], self.screen, 0, self.height, stretch=settings.surface_stretching, angles=angles,
                     closed=settings.closed_surface_contour, surface_height=settings.average_surface_height)
        utils.draw_shape([200 + l, 200], self.screen, pos1)

        utils.draw([300, 550], self.screen, pos2, alpha, self.height, stretch=settings.surface_stretching, angles=angles,
             closed=settings.closed_surface_contour, surface_height=settings.average_surface_height)

        pygame.display.flip()
