import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from Vector2D import Vector2D
import math
import matrixOps


polygonMatrix = None
intersectionMatrix = None


def intersectionSpreadFromPoint(point: Vector2D):
    n = 1000
    for i in range(n):
        line = getLineAtAngle(point, 2*i*math.pi/n)
        line0 = [p[0] for p in line]
        line1 = [p[1] for p in line]
        intersectionMatrix[line0, line1] = (i+1)/n


def getLineAtAngle(start: Vector2D, angle: float):
    # angle += math.pi/2
    angle %= 2 * math.pi

    if angle <= math.pi / 4 or angle > 7 * math.pi / 4:
        return getLineAtAngleShallowRight(start, angle)
    if 3 * math.pi / 4 < angle <= 5 * math.pi / 4:
        return getLineAtAngleShallowLeft(start, angle)
    if math.pi / 4 < angle <= 3 * math.pi / 4:
        return getLineAtAngleSteepUp(start, angle)
    if 5 * math.pi / 4 < angle <= 7 * math.pi / 4:
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

    newPoint = Vector2D(start.x + dx, math.floor(start.y + dy))
    while isWithinMatrixBounds(newPoint) and polygonMatrix[newPoint]:
        line.append(newPoint)
        dx += increment
        dy -= increment * tanAngle
        newPoint = Vector2D(start.x + dx, math.floor(start.y + dy))

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

    newPoint = Vector2D(math.floor(start.x + dx), start.y + dy)
    while isWithinMatrixBounds(newPoint) and polygonMatrix[newPoint]:
        line.append(newPoint)
        dy += increment
        dx -= increment * cotAngle
        newPoint = Vector2D(math.floor(start.x + dx), start.y + dy)

    return line


def isWithinMatrixBounds(point: Vector2D):
    return 0 <= point.x < polygonMatrix.shape[0] and 0 <= point.y < polygonMatrix.shape[1]


def main():
    dirname = 'bin/output_images/small/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'

    global polygonMatrix
    polygonMatrix = matrixOps.openImageAsBooleanMatrix(dirname + filename + extension)
    global intersectionMatrix
    intersectionMatrix = np.zeros(polygonMatrix.shape)

    intersectionSpreadFromPoint(Vector2D(100, 100))

    f0 = plt.figure(0)
    plt.imshow(polygonMatrix + intersectionMatrix)
    plt.show()

if __name__ == '__main__':
    main()