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
    color = (0, 0, 0)
    for i in range(len(pos) - 1):
        pygame.draw.line(screen, color, [pos[i][0] + center_position[0], pos[i][1] + center_position[1]],
                         [pos[i + 1][0] + center_position[0], pos[i + 1][1] + center_position[1]],
                         settings.line_thickness)
    pygame.draw.line(screen, color, [pos[-1][0] + center_position[0], pos[-1][1] + center_position[1]],
                     [pos[0][0] + center_position[0], pos[0][1] + center_position[1]], settings.line_thickness)
    dx = settings.r * alpha

    for i in range(len(height) - 1):
        color = (0, 0, 0)
        if angles is None:
            a = i * (2 * pi / settings.n)
        else:
            a = angles[i]
        pygame.draw.line(screen, color,
                         [-dx * stretch + a * settings.r * stretch + center_position[0],
                          height[i] + center_position[1]],
                         [-dx * stretch + stretch * a * settings.r + 1 + center_position[0],
                          height[i + 1] + center_position[1]],
                         settings.line_thickness)


def run():
    random_generated = settings.random_generated
    if random_generated:
        noiseGenerator = PerlinNoise()
        height = [settings.r + noiseGenerator(i * settings.perlin_noise_params[0]) * settings.perlin_noise_params[1] for i in
                  range(settings.n)]
        k = height[0] / height[-1]
        height = [height[i] * (1 + (k - 1) * (i / settings.n)) for i in range(len(height))]
    else:
        settings.r = settings.r
        settings.n = len(image_read.angle)

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
    try:
        settings.r = int(entrys[0].get())
        settings.n = int(entrys[1].get())
        settings.speed = float(entrys[2].get())
        settings.random_generated = entrys[3].get() in ['True', 'y', 'Y', '1', 'yes', 'Yes', 'YES', 'true', 't']
        settings.perlin_noise_params[0] = float(entrys[4].get())
        settings.perlin_noise_params[1] = float(entrys[5].get())
        settings.filename = entrys[6].get()
        settings.line_thickness = int(entrys[7].get())

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
             'k2 ("amplitude")', 'filename', 'line thickness']
    entrys_values = [str(settings.r), str(settings.n), str(settings.speed), str(settings.random_generated),
                     str(settings.perlin_noise_params[0]), str(settings.perlin_noise_params[1]), str(settings.filename),
                     str(settings.line_thickness)]

    labels = [tk.Label(root, text=text) for text in texts]
    entrys = [tk.Entry(root) for i in range(len(texts))]

    for i in range(len(texts)):
        labels[i].grid(row=i, column=0)
        entrys[i].insert(0, entrys_values[i])
        entrys[i].grid(row=i, column=1)

    button = tk.Button(root, text="Run", command=change_text)
    button.grid(row=len(texts), column=0)

    root.mainloop()
