from Vector2D import Vector2D
import numpy as np
from polygon import Polygon
import matplotlib.pyplot as plt

def polygonCollection(matrix: np.ndarray):
    polygons = list()
    neighbourhoods = floodFill(matrix)
    for neighbourhood in neighbourhoods:
        polygonMatrix = np.full(matrix.shape, False)
        unzipped_neighbourhood = tuple(zip(*neighbourhood))
        polygonMatrix[unzipped_neighbourhood] = True
        x_min = max(0, min(unzipped_neighbourhood[0])-1)
        x_max = min(polygonMatrix.shape[0], max(unzipped_neighbourhood[0])+2)
        y_min = max(0, min(unzipped_neighbourhood[1])-1)
        y_max = min(polygonMatrix.shape[1], max(unzipped_neighbourhood[1])+2)

        minimisedMatrix = polygonMatrix[x_min:x_max, y_min:y_max]

        polygons.append(Polygon(minimisedMatrix, Vector2D(x_min, y_min)))

    return polygons



def neighbouringPoints(pointList):
    neighbourhoods = list()
    visited = set()
    for point in pointList:
        if point not in visited:
            stack = list()
            neighbourhood = set()
            stack.append(point)
            while stack:
                curr = stack.pop()
                visited.add(curr)
                neighbourhood.add(curr)
                for neighbour in pointList:
                    if neighbour not in visited and curr.manhattan_distance_to(neighbour) <= 2:
                        stack.append(neighbour)
            neighbourhoods.append(neighbourhood)

    return neighbourhoods


def floodFill(matrix):
    loops = list()
    visited = set()
    stack = list()

    for ix, iy in np.ndindex(matrix.shape):
        curr = Vector2D(ix, iy)
        if matrix[curr] and curr not in visited:
            loop = list()
            stack.append(curr)
            visited.add(curr)
            while stack:
                curr = stack.pop()
                loop.append(curr)
                unvisitedNeighbours = getUnvisitedNeighbours(matrix, curr, visited)
                stack += unvisitedNeighbours
                visited.update(unvisitedNeighbours)

            loops.append(loop)

    return loops


def getUnvisitedNeighbours(matrix, curr, visited):
    neighbours = [curr + (1, 0), curr + (0, 1), curr + (-1, 0), curr + (0, -1),
                  curr + (1, 1), curr + (-1, -1), curr + (-1, 1), curr + (1, -1)]

    return [n for n in neighbours if indexIsWithinMatrix(n, matrix)
            and matrix[n] and n not in visited]


def indexIsWithinMatrix(index, matrix):
    return 0 <= index.x < matrix.shape[0] and 0 <= index.y < matrix.shape[1]
