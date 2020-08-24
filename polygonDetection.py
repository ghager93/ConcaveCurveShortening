from Vector2D import Vector2D
import numpy as np


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
                    if neighbour not in visited and curr.manhattanDistanceTo(neighbour) <= 2:
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
    neighbours = [curr + (1, 0), curr + (0, 1), curr + (-1, 0), curr + (0, -1)]

    return [n for n in neighbours if indexIsWithinMatrix(n, matrix)
            and matrix[n] and n not in visited]


def indexIsWithinMatrix(index, matrix):
    return 0 <= index.x < matrix.shape[0] and 0 <= index.y < matrix.shape[1]
