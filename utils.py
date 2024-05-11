import settings
from math import pi, sin, cos
import pygame


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


def draw_shape(center_position, screen, pos):
    """
    :param center_position: position of center of rotating figure
    :param screen: pygame screen
    :param pos: coordinates of points on the surface of a figure relative to its center
    :return: None
    """
    pygame.draw.lines(screen, settings.shape_color, True,
                      [[p[0] + center_position[0], p[1] + center_position[1]] for p in pos],
                      settings.line_thickness)


def draw_surface(center_position, screen, alpha, height, stretch=1.0, angles=None, closed=True, surface_height=100):
    """
    :param surface_height: average surface height
    :param closed: parameter responsible for whether a closed contour should be drawn
    :param angles: angles between vertical line and lines connecting center and the point on the surface of the figure
    :param height: distances from the center to the point on the surface of the figure
    :param center_position: position of center of rotating figure
    :param screen: pygame screen
    :param alpha: rotation angle of the construction
    :param stretch: surface tensile coefficient
    :return: None
    """
    dx = settings.r * alpha * stretch

    points = []

    for i in range(settings.n - 1):
        if angles is None:
            a = i * (2 * pi / settings.n)
        else:
            a = angles[i]
        points.append([-dx + a * settings.r * stretch + center_position[0], height[i] + center_position[1]])
    if closed:
        points.append([points[-1][0], center_position[1] + surface_height])
        points.append([points[0][0], center_position[1] + surface_height])
    pygame.draw.lines(screen, settings.shape_color, closed, points, settings.line_thickness)


def draw(center_position, screen, pos, alpha, height, stretch=1.0, angles=None, closed=True, surface_height=100):
    """
    :param surface_height: average surface height
    :param closed: parameter responsible for whether a closed contour should be drawn
    :param angles: angles between vertical line and lines connecting center and the point on the surface of the figure
    :param height: distances from the center to the point on the surface of the figure
    :param center_position: position of center of rotating figure
    :param screen: pygame screen
    :param pos: coordinates of points on the surface of a figure relative to its center
    :param alpha: rotation angle of the construction
    :param stretch: surface tensile coefficient
    :return: None
    """
    draw_shape(center_position, screen, pos)
    draw_surface(center_position, screen, alpha, height, stretch, angles, closed, surface_height)
