import cv2
import copy
import math
import pygame
import settings


def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def img_to_obj():
    global img2, angle
    img = cv2.imread(settings.filename)
    img2 = copy.deepcopy(img)

    l = []

    minX = img.shape[1]
    maxX = 0
    minY = img.shape[0]
    maxY = 0

    for i in range(1, len(img) - 1):
        for j in range(1, len(img[i]) - 1):
            if img[i][j][0] == 0:
                minX = min(minX, j)
                maxX = max(maxX, j)
                minY = min(minY, i)
                maxY = max(maxY, i)
            if img[i + 1][j][0] == 0 and img[i - 1][j][0] == 0 and img[i][j - 1][0] == 0 and img[i][j + 1][1] == 0:#and img[i + 1][j][1] == 0 and img[i + 1][j][2] == 2: #all([sum(i) == 0 for i in [img[i - 1][j], img[i + 1][j], img[i][j - 1], img[i][j + 1]]]):
                img2[i][j] = [255, 255, 255]
            elif img[i][j][0] == 0:
                img2[i][j] = [0, 0, 0]
                l.append([i, j])
            else:
                img2[i][j] = [255, 255, 255]

    center = [(minY + maxY) // 2, (minX + maxX) // 2]
    settings.r = min((maxX - minX) // 2, (maxY - minY) // 2)

    img2[center[0]][center[1]] = [255, 0, 0]

    angle = sorted([[math.atan2(i[0] - center[0], i[1] - center[1]), dist(*i, *center)] for i in l])
    return angle


if __name__ == '__main__':
    img_to_obj()
    cv2.imwrite("output.png", img2)

    pygame.init()
    size = [800, 800]
    screen = pygame.display.set_mode(size)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill([255, 255, 255])
        color = [0, 255, 255]
        for a, d in angle:
            pygame.draw.line(screen, color, [400, 400], [400 + math.sin(a) * d, 400 + math.cos(a) * d], 1)

        pygame.display.flip()
    pygame.quit()
