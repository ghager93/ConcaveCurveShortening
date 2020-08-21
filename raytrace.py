import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from Vector2D import Vector2D
import math


matrix = np.zeros((500, 500))

def drawLineAtAngle(start: Vector2D, angle: float):
    angle %= 2*math.pi

    if angle <= math.pi/4 or angle > 7*math.pi/4 or 3*math.pi/4 < angle <= 5*math.pi/4:
        drawLineAtAngleShallow(start, angle)
    else:
        drawLineAtAngleSteep(start, angle)


def drawLineAtAngleShallow(start: Vector2D, angle: float):
    tanAngle = math.tan(angle)
    dy = 0
    dx = 0
    while isWithinMatrixBounds(start + Vector2D(dx, dy)):
        matrix[start.x + dx, math.floor(start.y+dy)] = 1
        dx += 1
        dy += tanAngle


def drawLineAtAngleSteep(start: Vector2D, angle: float):
    cotAngle = 1 / math.tan(angle)
    dy = 0
    dx = 0
    while isWithinMatrixBounds(start + Vector2D(dx, dy)):
        matrix[math.floor(start.x + dx), start.y + dy] = 1
        dy += 1
        dx += cotAngle

#
# def isWithinMatrixBounds(point: Vector2D):
#     return point.x >= 0 and point.y >= 0 \
#            and point.x < matrix.shape[0] and point.y < matrix.shape[1]


def isWithinMatrixBounds(point: Vector2D):
    return 0 <= point.x < matrix.shape[0] and 0 <= point.y < matrix.shape[1]


if __name__ == '__main__':
    pass