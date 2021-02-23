import numpy as np

from bin.morphology.transforms import edge_transform
from bin.utils.vector2d import Vector2D
from bin.morphology.utils import neighbour_array

class EdgeLoop():
    def __init__(self, im: np.ndarray):
        self._im = np.pad(im, 1)
        self._im_edge = edge_transform(self._im)
        self._visited = set()
        self._start = self._starting_point()

    def _starting_point(self):
        edge_points = np.where(self._im_edge == 1)
        return Vector2D(edge_points[0][0], edge_points[1][0])

    def _second_point(self):
        starting_neighbourhood = self._neighbourhood(self._start)
        n = 0, 0

        if starting_neighbourhood[1, 2]:
            n = 0, 1
        if starting_neighbourhood[2, 2]:
            n = 1, 1
        if starting_neighbourhood[2, 1]:
            n = 1, 0

        return self._start + n

    def _last_point(self):
        starting_neighbourhood = self._neighbourhood(self._start)
        n = 0, 0
        if starting_neighbourhood[2, 0]:
            n =  1, -1
        if starting_neighbourhood[2, 1]:
            n = 1, 0
        if starting_neighbourhood[2, 2]:
            n = 1, 1

        return self._start + n

    def _neighbourhood(self, point: Vector2D):
        return self._im_edge[point.x-1:point.x+2, point.y-1:point.y+2]

    def _next_neighbour(self, point: Vector2D):
        neighbours = list()
        neighbourhood = self._neighbourhood(point)
        [neighbours.append(point + n) for n in neighbour_array.side_neighbour_coordinates(neighbourhood)]
        [neighbours.append(point + n) for n in neighbour_array.diagonal_neighbour_coordinates(neighbourhood)]

        neighbours = [n for n in neighbours if n not in self._visited]

        return neighbours[0] if neighbours else None

    def start(self):
        return self._unpad(self._start)

    def _unpad(self, point: Vector2D):
        return point - (1, 1)

    def _unpad_list(self, list):
        return [p - (1, 1) for p in list]

    def edge_loop(self):
        loop = [self._start]
        self._visited = set()
        self._visited.add(self._start)
        self._visited.add(self._last_point())

        curr = self._second_point()
        while curr:
            self._visited.add(curr)
            loop.append(curr)
            curr = self._next_neighbour(curr)
        loop.append(self._last_point())

        return self._unpad_list(loop)
