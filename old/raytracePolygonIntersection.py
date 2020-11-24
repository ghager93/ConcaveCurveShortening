import numpy as np
import matplotlib.pyplot as plt
from old.Vector2D import Vector2D
import math
from old import imageMatrix


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


def getLineAtAngleShallowLeft(start: Vector2D, matrix: np.ndarray, angle: float):
    return getLineAtAngleShallow(start, matrix, angle, -1)


def getLineAtAngleShallowRight(start: Vector2D, matrix: np.ndarray, angle: float):
    return getLineAtAngleShallow(start, matrix, angle, 1)


def getLineAtAngleShallow(start: Vector2D, matrix: np.ndarray, angle: float, increment: int):
    line = list()
    x_points = list()
    y_points = list()

    tanAngle = math.tan(angle)
    dy = 0
    dx = 0

    newPoint = Vector2D(start.x + dx, math.floor(start.y + dy))
    while isWithinMatrixBounds(newPoint, matrix) and matrix[newPoint]:
        line.append(newPoint)
        x_points.append(newPoint.x)
        y_points.append(newPoint.y)
        dx += increment
        dy -= increment * tanAngle
        newPoint = Vector2D(start.x + dx, math.floor(start.y + dy))

    return x_points, y_points


def getLineAtAngleSteepUp(start: Vector2D, matrix: np.ndarray, angle: float):
    return getLineAtAngleSteep(start, matrix, angle, -1)


def getLineAtAngleSteepDown(start: Vector2D, matrix: np.ndarray, angle: float):
    return getLineAtAngleSteep(start, matrix, angle, 1)


def getLineAtAngleSteep(start: Vector2D, matrix: np.ndarray, angle: float, increment: int):
    line = list()
    x_points = list()
    y_points = list()

    cotAngle = 1 / math.tan(angle)
    dy = 0
    dx = 0

    newPoint = Vector2D(math.floor(start.x + dx), start.y + dy)
    while isWithinMatrixBounds(newPoint, matrix) and matrix[newPoint]:
        line.append(newPoint)
        x_points.append(newPoint.x)
        y_points.append(newPoint.y)
        dy += increment
        dx -= increment * cotAngle
        newPoint = Vector2D(math.floor(start.x + dx), start.y + dy)

    return x_points, y_points


def isWithinMatrixBounds(point: Vector2D, matrix: np.ndarray):
    return 0 <= point.x < matrix.shape[0] and 0 <= point.y < matrix.shape[1]


def intersectingLinesFromPoint(point: Vector2D, matrix: np.ndarray):
    n = 1000
    new_matrix = np.full(matrix.shape, False)
    for i in range(n):
        angle = 2*i*math.pi/n
        new_matrix[getLineFunction(angle)(point, matrix, angle)] = True

    return new_matrix


def getLineFunction(angle):
    angle %= 2*math.pi

    if angle <= math.pi / 4 or angle > 7 * math.pi / 4:
        return getLineAtAngleShallowRight
    if 3 * math.pi / 4 < angle <= 5 * math.pi / 4:
        return getLineAtAngleShallowLeft
    if math.pi / 4 < angle <= 3 * math.pi / 4:
        return getLineAtAngleSteepUp
    if 5 * math.pi / 4 < angle <= 7 * math.pi / 4:
        return getLineAtAngleSteepDown


def main():
    dirname = 'out/output_images/small/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'

    im = imageMatrix.ImageMatrix.openImageAsBooleanMatrix(dirname + filename + extension)
    nm = intersectingLinesFromPoint(Vector2D(100, 100), im)

    f0 = plt.figure(0)
    plt.imshow(im.astype(int) + nm)
    plt.show()


if __name__ == '__main__':
    main()
