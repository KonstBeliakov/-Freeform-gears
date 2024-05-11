from perlin_noise import PerlinNoise
import pygame
from math import sin, cos, pi
from time import perf_counter
import image_read
import settings
import tkinter as tk
from math import pi


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
    :param surface_height:
    :param closed:
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


def run():
    random_generated = settings.random_generated
    if random_generated:
        noiseGenerator = PerlinNoise()
        height = [settings.r + noiseGenerator(i * settings.perlin_noise_params[0]) * settings.perlin_noise_params[1] for i in
                  range(settings.n)]
        k = height[0] / height[-1]
        height = [height[i] * (1 + (k - 1) * (i / settings.n)) for i in range(len(height))]
        angles = None
    else:
        settings.r = settings.r
        settings.n = len(image_read.angle)

        height = [i[1] for i in image_read.angle]
        angles = [i[0] for i in image_read.angle]

    pygame.init()

    size = settings.screen_size
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # screen = pygame.display.set_mode(size)

    run = True

    t = perf_counter()
    t_speed = settings.speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(settings.background_color)
        alpha = (perf_counter() - t) * t_speed

        pos1 = position(height, 0, angles=angles)
        pos2 = position(height, -alpha, angles=angles)

        if random_generated:
            angles = None

        l = settings.r * settings.surface_stretching * pi * 2

        draw_surface([50, 100], screen, 0, height, stretch=settings.surface_stretching, angles=angles,
                     closed=settings.closed_surface_contour, surface_height=settings.average_surface_height)
        draw_shape([200 + l, 200], screen, pos1)

        draw([300, 550], screen, pos2, alpha, height, stretch=settings.surface_stretching, angles=angles,
             closed=settings.closed_surface_contour, surface_height=settings.average_surface_height)

        pygame.display.flip()
    pygame.quit()


def apply_settings():
    try:
        settings.r = int(entrys[0].get())
        settings.n = int(entrys[1].get())
        settings.speed = float(entrys[2].get())
        settings.random_generated = entrys[3].get() in ['True', 'y', 'Y', '1', 'yes', 'Yes', 'YES', 'true', 't']
        settings.perlin_noise_params[0] = float(entrys[4].get())
        settings.perlin_noise_params[1] = float(entrys[5].get())
        settings.filename = entrys[6].get()
        settings.line_thickness = int(entrys[7].get())
        settings.surface_stretching = float(entrys[8].get())
        settings.closed_surface_contour = entrys[9].get() in ['True', 'y', 'Y', '1', 'yes', 'Yes', 'YES', 'true', 't']
        settings.average_surface_height = int(entrys[10].get())

        if not settings.random_generated:
            image_read.img_to_obj()
    except:
        error_text = tk.Label(root, text='Incorrect settings parametres', fg='#f00')
        error_text.grid(row=len(texts) + 1, column=0)
        return False
    else:
        return True


def change_text():
    if apply_settings():
        root.destroy()
        run()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Settings")

    texts = ['radius of random figure', 'number of point', 'speed', 'random generated figure (y/n)', 'k1 ("period")',
             'k2 ("amplitude")', 'filename', 'line thickness', 'surface stretching', 'closed surface contour (y/n)',
             'average surface height']
    entrys_values = [str(settings.r), str(settings.n), str(settings.speed), str(settings.random_generated),
                     str(settings.perlin_noise_params[0]), str(settings.perlin_noise_params[1]), str(settings.filename),
                     str(settings.line_thickness), str(settings.surface_stretching),
                     str(settings.closed_surface_contour), str(settings.average_surface_height)]

    labels = [tk.Label(root, text=text) for text in texts]
    entrys = [tk.Entry(root) for i in range(len(texts))]

    for i in range(len(texts)):
        labels[i].grid(row=i, column=0)
        entrys[i].insert(0, entrys_values[i])
        entrys[i].grid(row=i, column=1)

    button = tk.Button(root, text="Run", command=change_text)
    button.grid(row=len(texts), column=0)

    root.mainloop()
