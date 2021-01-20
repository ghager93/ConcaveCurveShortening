import numpy as np
import math

from bin.utils.vector2d import Vector2D
from bin.utils.imshow import show, show_multiple


# https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def bresenham(p1: Vector2D, p2: Vector2D):
    deltax = p2.x - p1.x
    deltay = p2.y - p1.y
    if deltax != 0:
        deltaerr = abs(deltay / deltax)
    else:
        deltaerr = math.nan

    def _delta_error_less_than_one():
        y = p1.y
        error = 0
        line = []
        for x in _line_range(p1.x, p2.x):
            line.append(Vector2D(x, y))
            error += deltaerr
            if error >= 0.5:
                y += np.sign(deltay)
                error -= 1

        return line

    def _delta_error_greater_than_or_equal_to_one():
        inv_deltaerr = 1 / deltaerr
        x = p1.x
        error = 0
        line = []
        for y in _line_range(p1.y, p2.y):
            line.append(Vector2D(x, y))
            error += inv_deltaerr
            if error >= 0.5:
                x += np.sign(deltax)
                error -= 1

        return line

    def _delta_error_zero():
        # x_range = range(p1.x, p2.x) if p2.x >= p1.x else reversed(range(p2.x, p1.x))
        return [Vector2D(x, p1.y) for x in _line_range(p1.x, p2.x)]

    def _delta_error_undefined():
        # y_range = range(p1.y, p2.y) if p2.y >= p1.y else reversed(range(p2.y, p1.y))
        return [Vector2D(p1.x, y) for y in _line_range(p1.y, p2.y)]

    if deltaerr >= 1:
        line = _delta_error_greater_than_or_equal_to_one()
    if deltaerr < 1:
        line = _delta_error_less_than_one()
    if deltaerr == 0:
        line = _delta_error_zero()
    if math.isnan(deltaerr):
        line = _delta_error_undefined()

    return line


def _draw_line(p1: Vector2D, p2: Vector2D):
    mat = _normalised_line_as_matrix(p1, p2)
    show(np.pad(mat, 1))


def _normalised_line_as_matrix(p1: Vector2D, p2: Vector2D):
    p1, p2 = _normalise_points(p1, p2)
    line = bresenham(p1, p2)
    mat = np.zeros((abs(p1.x-p2.x)+1, abs(p1.y-p2.y)+1), int)
    mat[tuple(p for p in zip(*line))] = 1
    mat[p1] = 2
    mat[p2] = 2

    return np.pad(mat, 1)


def _normalise_points(p1, p2):
    minx = min(p1.x, p2.x)
    miny = min(p1.y, p2.y)

    return Vector2D(p1.x - minx, p1.y - miny), Vector2D(p2.x - minx, p2.y - miny)


def _draw_lines_of_circle(p: Vector2D, r: float, num=16):
    show_multiple([_normalised_line_as_matrix(p, Vector2D(int(r * np.cos(theta)), int(r * np.sin(theta))) + p)
                   for theta in np.linspace(0, 2*np.pi, num=num, endpoint=False)])


def _line_range(start, end):
    return range(start, end) if end >= start else reversed(range(end, start))


if __name__ == '__main__':
    a = Vector2D(2, 4)
    _draw_lines_of_circle(a, 10)


