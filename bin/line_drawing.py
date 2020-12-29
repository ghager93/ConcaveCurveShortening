import numpy as np
import math

from bin.util.vector2d import Vector2D
from bin.image_array import show


def bresenham(p1: Vector2D, p2: Vector2D):
    deltax = p2.x - p1.x
    deltay = p2.y - p1.y
    deltaerr = abs(deltay / deltax)

    y = p1.y
    error = 0
    line = []
    for x in range(p1.x, p2.x):
        line.append(Vector2D(x, y))
        error += deltaerr
        if error >= 0.5:
            y += np.sign(deltay)
            error -= 1

    return line


def draw_line(p1: Vector2D, p2: Vector2D):
    p1, p2 = _normalise_points(p1, p2)
    line = bresenham(p1, p2)
    mat = np.zeros((abs(p1.x-p2.x)+1, abs(p1.y-p2.y)+1), int)
    mat[tuple(p for p in zip(*line))] = 1
    show(np.pad(mat, 1))


def _normalise_points(p1, p2):
    minx = min(p1.x, p2.x)
    miny = min(p1.y, p2.y)

    return Vector2D(p1.x - minx, p1.y - miny), Vector2D(p2.x - minx, p2.y - miny)


def draw_lines_of_circle(p: Vector2D, r: float):
    for theta in np.linspace(0, 2*np.pi, num=100):
        draw_line(p, Vector2D(int(r * np.cos(theta)), int(r * np.sin(theta))) + p)


if __name__ == '__main__':
    a = Vector2D(2, 4)
    draw_lines_of_circle(a, 10)


