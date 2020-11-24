import numpy as np
import matplotlib.pyplot as plt
from old.Vector2D import Vector2D
import math


matrix = np.zeros((500, 500))


def drawLineAtAngle(start: Vector2D, angle: float, value: float = 1.):
    for p in getLineAtAngle(start, angle):
        matrix[p] = value


def getLineAtAngle(start: Vector2D, angle: float):
    # angle += math.pi/2
    angle %= 2*math.pi

    if angle <= math.pi/4 or angle > 7*math.pi/4:
        return getLineAtAngleShallowRight(start, angle)
    if 3*math.pi/4 < angle <= 5*math.pi/4:
        return getLineAtAngleShallowLeft(start, angle)
    if math.pi/4 < angle <= 3*math.pi/4:
        return getLineAtAngleSteepUp(start, angle)
    if 5*math.pi/4 < angle <= 7*math.pi/4:
        return getLineAtAngleSteepDown(start, angle)


def getLineAtAngleShallowLeft(start: Vector2D, angle: float):
    return getLineAtAngleShallow(start, angle, -1)
    
    
def getLineAtAngleShallowRight(start: Vector2D, angle: float):
    return getLineAtAngleShallow(start, angle, 1)


def getLineAtAngleShallow(start: Vector2D, angle: float, increment: int):
    line = list()

    tanAngle = math.tan(angle)
    dy = 0
    dx = 0
    while isWithinMatrixBounds(start + Vector2D(dx, dy)):
        line.append(Vector2D(start.x + dx, math.floor(start.y+dy)))
        dx += increment
        dy -= increment * tanAngle

    return line


def getLineAtAngleSteepUp(start: Vector2D, angle: float):
    return getLineAtAngleSteep(start, angle, -1)
    
    
def getLineAtAngleSteepDown(start: Vector2D, angle: float):
    return getLineAtAngleSteep(start, angle, 1)
    

def getLineAtAngleSteep(start: Vector2D, angle: float, increment: int):
    line = list()

    cotAngle = 1 / math.tan(angle)
    dy = 0
    dx = 0
    while isWithinMatrixBounds(start + Vector2D(dx, dy)):
        line.append(Vector2D(math.floor(start.x + dx), start.y + dy))
        dy += increment
        dx -= increment * cotAngle

    return line


def isWithinMatrixBounds(point: Vector2D):
    return 0 <= point.x < matrix.shape[0] and 0 <= point.y < matrix.shape[1]


if __name__ == '__main__':
    for i in range(1, 500):
        drawLineAtAngle(Vector2D(250, 250), i*math.pi/249, i/500)

    plt.imshow(matrix.transpose())
    plt.show()