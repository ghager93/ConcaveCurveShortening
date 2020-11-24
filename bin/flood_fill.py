import numpy as np

from bin.polygon import Polygon, PolygonArray
from bin.util.vector2d import Vector2D


class _FloodFillObject:
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.visited = set()
        self.stack = list()

    def get_polygons(self):
        polygons = list()
        self.visited = set()
        for ix, iy in np.ndindex(self.matrix.shape):
            start = Vector2D(ix, iy)
            if self.is_non_zero(start) and self.is_unvisited(start):
                polygons.append(Polygon(self.get_points_in_polygon_by_dfs(start)))

        return polygons

    def get_points_in_polygon_by_dfs(self, start: Vector2D):
        points = list()
        self.stack = list()
        self.add_point_to_stack_and_visited_if_legal_and_unvisited(start)
        while self.stack:
            curr = self.stack.pop()
            points.append(curr)
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (1, 0))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (-1, 0))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (0, 1))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (0, -1))

        return points

    def is_unvisited(self, point: Vector2D):
        return point not in self.visited

    def is_in_matrix(self, point: Vector2D):
        return 0 <= point.x < self.matrix.shape[0] and \
               0 <= point.y < self.matrix.shape[1]

    def is_non_zero(self, point: Vector2D):
        return self.matrix[point]

    def is_legal(self, point: Vector2D):
        return self.is_in_matrix(point) and self.is_non_zero(point)

    def add_point_to_stack_and_visited_if_legal_and_unvisited(self, point: Vector2D):
        if self.is_legal(point) and self.is_unvisited(point):
            self.visited.add(point)
            self.stack.append(point)


def get_polygons(matrix: np.ndarray):
    return _FloodFillObject(matrix).get_polygons()


def get_polygon_arrays(matrix: np.ndarray):
    return [PolygonArray.from_polygon(polygon) for polygon in get_polygons(matrix)]