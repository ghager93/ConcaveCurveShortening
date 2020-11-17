import numpy as np

from bin.util.vector2d import Vector2D


class PolygonBoundary:
    def __init__(self, points):
        self.xmin = self._find_xmin_from_points(points)
        self.ymin = self._find_ymin_from_points(points)
        self.xmax = self._find_xmax_from_points(points)
        self.ymax = self._find_ymax_from_points(points)

    def upper_left(self):
        return Vector2D(self.xmin, self.ymin)

    def lower_right(self):
        return Vector2D(self.xmax, self.ymax)

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    def shape(self):
        return self.width(), self.height()

    def size(self):
        return self.width() * self.height()

    @staticmethod
    def _find_xmin_from_points(points):
        return min([p[0] for p in points])

    @staticmethod
    def _find_xmax_from_points(points):
        return max([p[0] for p in points])

    @staticmethod
    def _find_ymin_from_points(points):
        return min([p[1] for p in points])

    @staticmethod
    def _find_ymax_from_points(points):
        return max([p[1] for p in points])


class Polygon(PolygonBoundary):
    def __init__(self, points):
        self.points = points
        super().__init__(points)

    def as_array(self):
        array = np.zeros(self.shape())
        for point in self.points:
            array[point - self.upper_left()] = 1

        return array


class PolygonArray(PolygonBoundary):
    def __init__(self, points):
        super().__init__(points)
        self.array = self._make_array_from_points(points)

    @classmethod
    def from_polygon(cls, polygon: Polygon):
        return cls(polygon.points)

    def _make_array_from_points(self, points):
        array = np.zeros(self.shape())
        rows, cols = zip(*points)
        array[rows, cols] = 1

        return array
